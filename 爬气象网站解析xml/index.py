

import xml.etree.ElementTree as ET
import pprint
pro_Name=["leixi","caption",None,None,"date_time",
          "temperature","date_weather","wind",
          None,None,
          "weather_details",
          "weather_others",
          #昨天情况
          "yesterday_temperature",
          "yesterday_date_time","yesterday_wind",
          None,None,
          #明天情况
          "tomorrow_temperature",
          "tomorrow_date_time","tomorrow_wind",
          None,None,
          "caption_summary"]
weather_dic={}
def parse_xml():
    xmlTree = ET.parse("weather.xml")
    root = xmlTree.getroot()
    for i in range(len(pro_Name)):
        weather_dic[pro_Name[i]]=root[i].text

def ret_quest(request):
    if request == "help":
        return pro_Name
    elif request not in weather_dic:
        return "句柄不正确"
    else:
        return weather_dic[request]

def main():
    caption="上海"
    from urllib import request
    handle = request.quote(caption)
    weather_url = "http://www.webxml.com.cn/WebServices/WeatherWebService.asmx/getWeatherbyCityName?theCityName=%s" % handle
    urlObj = request.urlopen(weather_url)
    xml_part = str(urlObj.read(), encoding="utf8")
    with open("weather.xml", "w", encoding="utf-8") as f:
        f.write(xml_part)
    parse_xml()
    while True:
        request=input("请输入你要查看天气的哪方面/[help]查看句柄/exit退出:")
        if request == "exit":
            break
        result=ret_quest(request)
        print(result)
main()