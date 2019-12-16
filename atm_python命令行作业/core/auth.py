
from conf import setting
import random
from core.hash_factory import hash_factory


def login2(db_manager):
    '''
    the function use to login,get a userlist,to compare cardNum and passwd
     loop to input,passwd only three times,then frozed,return user and flag,
     or cannot find cardNum then loop,input exit then return exit and flag
    :param db_manager:
    :return:
    '''

    db_manager.make_db(setting.DB_NAME,setting.DB_TYPE)
    count = 3
    while True:
        cardNum = input("请输入卡号([exit]退出):")
        if cardNum in db_manager.CARD_GROUP:
            if db_manager.USER_MSG_DICT[cardNum]["userstatu"] == False:
                return cardNum,"froze"
            while count > 0:
                passwd = input("请输入密码:")
                passwd=hash_factory(passwd)
                if passwd == db_manager.USER_MSG_DICT[cardNum]["passwd"]:
                    if db_manager.USER_MSG_DICT[cardNum]["loginstatu"]:
                        print('''%s先生,您已经登录,卡号是%s'''%
                              (db_manager.USER_MSG_DICT[cardNum]["name"],cardNum))
                    else:
                        print("登录成功")
                        # change login status
                        db_manager.USER_MSG_DICT[cardNum]["loginstatu"] = True
                    return cardNum,True
                else:
                    count -= 1
                    print("密码不正确，还有%d此机会" % count)
            else:
                print("您已经不能在输入了,正在处理")
                return cardNum,"froze"
        elif cardNum == "exit":
            return None,False
        else:
            print("没有此卡号,请重新输入")


def login(db_manager):
    '''
    the function use to login,get a userlist,to compare cardNum and passwd
     loop to input,passwd only three times,then frozed,return user and flag,
     or cannot find cardNum then loop,input exit then return exit and flag
    :param db_manager:
    :return:
    '''
    count = 3
    while True:
        cardNum = input("请输入卡号([exit]退出):")

        if cardNum in db_manager.CARD_GROUP:
            db_manager.make_db(cardNum,setting.DB_TYPE)
            if db_manager.USER_MSG_DICT[cardNum]["userstatu"] == False:
                return cardNum, "froze"

            # 贷款超时判断
            import datetime
            expiration_time=datetime.datetime.strptime(db_manager.USER_MSG_DICT[cardNum]["expiration_time"],
            "%Y-%m-%d %H:%M:%S.%f") if db_manager.USER_MSG_DICT[cardNum]["expiration_time"] else None
            print(expiration_time)
            print(expiration_time > datetime.datetime.now())
            if expiration_time:
                if expiration_time < datetime.datetime.now():
                    return cardNum, "froze"


            while count > 0:
                passwd = input("请输入密码:")
                passwd = hash_factory(passwd)
                if passwd == db_manager.USER_MSG_DICT[cardNum]["passwd"]:
                    if db_manager.USER_MSG_DICT[cardNum]["loginstatu"]:
                        print('''%s先生,您已经登录,卡号是%s''' %
                              (db_manager.USER_MSG_DICT[cardNum]["name"], cardNum))
                    else:
                        print("登录成功")
                        # change login status
                        db_manager.USER_MSG_DICT[cardNum]["loginstatu"] = True
                        print(db_manager.USER_MSG_DICT)
                    return cardNum, True
                else:
                    count -= 1
                    print("密码不正确，还有%d此机会" % count)
            else:
                print("您已经不能在输入了,正在处理")
                return cardNum, "froze"
        elif cardNum == "exit":
            return None, False
        else:
            print("没有此卡号,请重新输入")


def logout(db_manager,cardNum):
    '''
    登出账户
    :param db_manager:
    :param cardNum:
    :return:
    '''
    db_manager.USER_MSG_DICT[cardNum]["loginstatu"]=False
    db_manager.write_to_db(cardNum,setting.DB_TYPE)

def froze(cardNUM,db_manager):
    '''
    the function  froze user(冻结帐号)
    :param user:
    :return:
    '''
    if db_manager.USER_MSG_DICT[cardNUM]["loginstatu"]:
        db_manager.USER_MSG_DICT[cardNUM]["loginstatu"] = False
    if db_manager.USER_MSG_DICT[cardNUM]["userstatu"]:
        db_manager.USER_MSG_DICT[cardNUM]["userstatu"] = False
    print("您的账户已经冻结，请到人工服务处申请解冻")

def register(db_manager):
    '''
    register function
    :param db_manager:
    :return:
    '''
    print("正在注册")
    name=input("请输入你的名字:")
    passwd, IDcard,cardNum=None,None,None
    while True:
        passwd=input("请输入卡密码%s位:"%setting.USER_PASS_LEN)
        if len(passwd) != setting.USER_PASS_LEN or not passwd.isdigit():
            print("密码格式错误请重新输入")
        else:
            while True:
                pass02=input("请再次输入卡密码:")
                if passwd != pass02:
                    print("两次输入不一致")
                else:
                    print("密码输入正确")
                    break
            passwd = hash_factory(passwd)
            break
    while True:
        IDcard=input("请输入您的身份证%s位"%setting.CARD_ID_LEN)
        if len(IDcard) != setting.CARD_ID_LEN:
            print("身份证格式错误")
        else:
            break
    birth=input("请输入您的生日[%s]"%setting.DATE_FORMAT)
    account=input("请输入存储的金额[默认15000]")
    account=account if account else 15000
    while True:
        cardNum=make_cardNum()
        if cardNum not in db_manager.CARD_GROUP:
            break
    db_manager.USER_MSG_DICT.clear()
    db_manager.USER_MSG_DICT[cardNum] = {
        "passwd":passwd,
        "name":name,
        "IDcard":IDcard,
        "birth":birth,
        "account":account,
        "userstatu":True,
        "loginstatu":False,
        "exceed": None,
        "expiration time": None
    }
    print('''
        %s先生,
        您输入的信息无误,您的卡号是：
         %s
         请等待录入
        ''' % (db_manager.USER_MSG_DICT[cardNum]["name"], cardNum))
    return cardNum



def make_cardNum():
    '''
    创建卡号,不重复的卡号
    :return:
    '''
    cardNum=""
    for i in range(setting.CARD_NUM_ID):
        cardNum+=str(random.randrange(0,10))
    return cardNum

def auth(db_manager):
    '''此函数获取当前用户名
    在每次操作金额时，判断一下，仅仅判断一次
    cardCheck:如果卡号已经确认，不用输入卡号
    '''
    def wrapper(func):
        def inner(cardNUM,*args,**kwargs):
            count = 3
            while count > 0:
                passwd=input("请输入您的密码：")
                passwd=hash_factory(passwd)
                if passwd == db_manager.USER_MSG_DICT[cardNUM]["passwd"]:

                    print("登录成功，您的余额还有%s"%db_manager.USER_MSG_DICT[cardNUM]["account"])
                    temp = func(cardNUM,*args,**kwargs)
                    print("您的余额还有%s"%db_manager.USER_MSG_DICT[cardNUM]["account"])
                    break
                else:
                    count-=1
                    print("密码错误，还有%s次机会"%count)
            else:
                db_manager.USER_MSG_DICT[cardNUM]["loginstatu"] = False
                db_manager.USER_MSG_DICT[cardNUM]["userstatu"] = False
                temp = False
            return temp
        return inner
    return wrapper