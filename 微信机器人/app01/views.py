from django.shortcuts import render, HttpResponse

import requests
import re
import time
import json
from bs4 import BeautifulSoup




def login(req):
    if req.method == "GET":

        resp01 = requests.get("https://wx.qq.com/?&lang=zh_CN")
        timestamp = int(time.time() * 100)

        index_cookie = resp01.cookies.get_dict()


        jslogin_resp = requests.get("https://login.wx.qq.com/jslogin",
                                    params={
                                        "appid": "wx782c26e4c19acffb",
                                        "redirect_uri": "https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage",
                                        "fun": "new",
                                        "lang": "zh_CN",
                                        "_": timestamp
                                    }, cookies=index_cookie)

        jslogin_cookie = jslogin_resp.cookies.get_dict()

        qrcode = re.findall("window.QRLogin.code = 200; window.QRLogin.uuid = \"(.*)\";", jslogin_resp.text)[0]


        return render(req, "login.html", {"qrcode": qrcode, "timestamp": timestamp})

def jslogin(req):

    qrcode = req.GET.get("qrcode")
    timestamp = int(req.GET.get("timestamp")) + 1
    tip = int(req.GET.get("tip"))
    login_resp = requests.get("https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login",
                              params={
                                  "loginicon": "true",
                                  "uuid": qrcode,
                                  "tip": tip,
                                  "r": -1454498946,
                                  "_": timestamp,
                              })

    res_dict = {
        "code": "",
    }
    login_resp_list = login_resp.text.split(";", 1)

    code_reg = re.compile(r"window.code=(.*)")
    userAvatar_reg = re.compile(r"window.userAvatar = '(.*)';")
    redirect_uri_reg = re.compile(r"window.redirect_uri=\"(.*)\";")

    res_dict["code"] = code_reg.findall(login_resp_list[0])[0]
    if res_dict["code"] == "408":
        pass
    elif res_dict["code"] == "201":
        res_dict["userAvatar"] = userAvatar_reg.findall(login_resp_list[1])[0]
    elif res_dict["code"] == "200":
        res_dict["redirect_uri"] = redirect_uri_reg.findall(login_resp_list[1])[0] + "&fun=new&version=v2&lang=zh_CN"
        res_dict["cookies"] = json.dumps(login_resp.cookies.get_dict())

    elif res_dict["code"] == "400":
        pass


    return HttpResponse(json.dumps(res_dict))


def get_redirect_uri(req):
    if req.method == 'POST':
        redirect_uri = req.POST.get("redirect_uri")
        redirect_uri_resp = requests.get(redirect_uri)
        print(redirect_uri_resp.url)

        req.session["redirect_uri_cookies"] = redirect_uri_resp.cookies.get_dict()


        xml_dict = {}

        bs4_obj = BeautifulSoup(redirect_uri_resp.text, "html.parser")

        for tag in bs4_obj.find("error").children:

            xml_dict[tag.name] = tag.text



        req.session["init_xml"] = xml_dict



        return HttpResponse("success")

def webwxinit(req):


    init_xml = req.session["init_xml"]
    cookies = req.session["redirect_uri_cookies"]



    #
    webwxinit_resp = requests.post("https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxinit",
                 params={
                     "r": "-1471673265",
                     "pass_ticket": init_xml["pass_ticket"],
                 },
                 json={
                     "BaseRequest":{
                        "DeviceID": "e208267712107989",
                        "Sid": init_xml["wxsid"],
                        "Skey": init_xml["skey"],
                        "Uin": init_xml["wxuin"]
                    }
                 },)

    webwxinit_resp.encoding = "UTF-8"
    other_person_list = json.loads(webwxinit_resp.text)


    #
    #
    # req.session["redirect_uri_cookies"] = cookies
    # req.session["webwxinit_resp"] = webwxinit_resp.text
    # req.session["webwxinit_resp_cookies"] = webwxinit_resp.cookies

    contact_person_list_resp = requests.get("https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxgetcontact",
                                       params={
                                           "lang": "zh_CN",
                                           "pass_ticket": init_xml["pass_ticket"],
                                           "r": "1509022371437",
                                           "seq": "0",
                                           "skey": init_xml["skey"]
                                       }, cookies=cookies)
    contact_person_list_resp.encoding = "UTF-8"

    contact_person_list = json.loads(contact_person_list_resp.text)






    return render(req, "index.html", {"other_person_list": other_person_list,
                                      "contact_person_list": contact_person_list})


def webwxgeticon(req):
    url = req.GET.get("url")
    username = req.GET.get("username")
    skey = req.GET.get("skey")

    #cookies很重要，是扫码成功后的cookies
    cookies = req.session["redirect_uri_cookies"]

    url_img_resp = requests.get("https://wx.qq.com%s&username=%s&skey=%s" % (url,
                                             username, skey),
                                headers={
                                    "Referer": "https://wx.qq.com/?&lang=zh_CN",
                                },
                                cookies=cookies)


    return HttpResponse(url_img_resp.content)

def sendMsg(req):
    msgInp = req.POST.get("msgInp")
    from_user = req.POST.get("from_user")
    to_user = req.POST.get("to_user")

    init_xml = req.session["init_xml"]

    print(msgInp, from_user, to_user)

    timestamp = int(time.time() * 100)

    cookies = req.session["redirect_uri_cookies"]

    send_data = {
      "BaseRequest": {
          "DeviceID": "e208267712107989",
        "Sid": init_xml["wxsid"],
        "Skey": init_xml["skey"],
        "Uin": init_xml["wxuin"]
      },
      "Msg":{
          "ClientMsgId": timestamp,
          "Content": msgInp,
          "FromUserName": from_user,
          "LocalID": timestamp,
          "ToUserName": to_user,
          "Type": 1
      },
      "Scene":0
  }

    send_data_tmp = json.dumps(send_data, ensure_ascii=False).encode("utf-8")
    print(send_data_tmp)

    smsg_resp = requests.post("https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsendmsg?lang=zh_CN",
                              data=send_data_tmp,

                              cookies=cookies,
                              headers={
                                  "Referer": "https://wx.qq.com/?&lang=zh_CN",
                                  "Content-Type": "application/json",
                              },
                              )

    print(smsg_resp.text)
    print(smsg_resp.request.body)


    return HttpResponse("....")