from conf import setting
from core import db_manager
from core import auth
from core import account_factory
from core import pause_func
from core import logger

NOW_USER={"now_card":None}
def login():
    '''
    登录接口
    :return:
    '''
    cardNUM,judge=auth.login(db_manager)
    if not cardNUM:
        return None,judge
    elif cardNUM == "froze":
        return cardNUM,"froze"
    else:
        NOW_USER["now_card"]=cardNUM
        return cardNUM,judge
def froze(card_num):
    '''
    冻结账户
    :return:
    '''
    auth.froze(card_num,db_manager)
    db_manager.write_to_db(card_num,setting.DB_TYPE)
def register():
    card_num =auth.register(db_manager)
    try:
        db_manager.write_to_db(card_num, setting.DB_TYPE)
    except Exception:
        pass
    else:
        print("录入信息成功")

def logout(card_num):
    auth.logout(db_manager,card_num)
    db_manager.write_to_db(card_num, setting.DB_TYPE)

@auth.auth(db_manager)
def deposit(card_num):
    '''
    存款
    :param cardNUM:
    :return:
    '''
    db_manager.make_db(card_num, setting.DB_TYPE)
    diff_res = int(input("您要存多少："))
    account = int(db_manager.USER_MSG_DICT[card_num]["account"])
    account = account_factory.change_account(account,diff_res,sign="+")
    db_manager.USER_MSG_DICT[card_num]["account"] = str(account)
    db_manager.write_to_db(card_num, setting.DB_TYPE)


@auth.auth(db_manager)
def withdraw(card_num):
    '''
    取款
    :param cardNUM:
    :return:
    '''
    db_manager.make_db(card_num, setting.DB_TYPE)
    while True:
        diff_res = int(input("您要取多少："))
        account = int(db_manager.USER_MSG_DICT[card_num]["account"])
        if diff_res > account:
            print("您的余额透支，请走贷款渠道")
            c_flag=input("是否走贷款渠道").strip()
            if c_flag == "Y":
                credit(card_num)
        account = account_factory.change_account(account, diff_res, sign="-")
        db_manager.USER_MSG_DICT[card_num]["account"] = str(account)
        db_manager.write_to_db(card_num, setting.DB_TYPE)
        return True

def toBalance(salary):
    if not NOW_USER["now_card"]:
        login()
    account = int(db_manager.USER_MSG_DICT[NOW_USER["now_card"]]["account"])
    if salary > account:
        print("您的余额透支，请走贷款渠道")
        c_flag = input("是否走贷款渠道").strip()
        if c_flag == "Y":
            credit(salary)
    account = account_factory.change_account(account, salary, sign="-")
    db_manager.USER_MSG_DICT[NOW_USER["now_card"]]["account"] = str(account)
    db_manager.write_to_db(setting.DB_NAME, setting.DB_TYPE)
    return account

@auth.auth(db_manager)
def transfer(from_card_num):
    '''
    转账，条件：对方用户没有被冻结，和对方用户已经在线
    :param from_cardNUM:
    :return:
    '''
    db_manager.make_db(from_card_num, setting.DB_TYPE)
    to_card_num=None

    #保存两个用户的信息
    from_user_dict = {}
    # 这个变量必须另外开辟一条空间,否则这个变量如果引用USER_MSG_DICT,会牵着鼻子走
    # from_user_dict = db_manager.USER_MSG_DICT
    from_user_dict.update(db_manager.USER_MSG_DICT)
    to_user_dict={}
    while True:
        to_card_num=input("您要转给谁：")
        if to_card_num == "exit":
            return to_card_num

        if to_card_num not in db_manager.CARD_GROUP:
            print("卡号不存在，请重新输入")
        else:
            db_manager.make_db(to_card_num)
            to_user_dict.update(db_manager.USER_MSG_DICT)
            break

    if to_user_dict[to_card_num]["loginstatu"] == True and \
        to_user_dict[to_card_num]["userstatu"] == True:
        from_account = int(from_user_dict[from_card_num]["account"])
        to_account = int(to_user_dict[to_card_num]["account"])
        diff_res=int(input("您要转多少："))
        from_account = account_factory.change_account(from_account, diff_res, sign="-")
        to_account = account_factory.change_account(to_account, diff_res, sign="+")
        from_user_dict[from_card_num]["account"] = str(from_account)
        to_user_dict[to_card_num]["account"] = str(to_account)
        # 先保存对方账户,删除零时字典,更新临时字典为本账户,再保存
        db_manager.USER_MSG_DICT.clear()
        db_manager.USER_MSG_DICT.update(to_user_dict)
        db_manager.write_to_db(to_card_num, setting.DB_TYPE)

        db_manager.USER_MSG_DICT.clear()
        db_manager.USER_MSG_DICT.update(from_user_dict)
        db_manager.write_to_db(from_card_num, setting.DB_TYPE)
        return True
    elif to_user_dict[to_card_num]["userstatu"] == False:
        print("%s用户已经冻结"%db_manager.USER_MSG_DICT[to_card_num]["name"])
    elif to_user_dict[to_card_num]["loginstatu"] == False:
        print("%s用户还没登陆" % db_manager.USER_MSG_DICT[to_card_num]["name"])
    db_manager.USER_MSG_DICT.clear()
    db_manager.USER_MSG_DICT.update(from_user_dict)


def credit(card_num):
    '''
    一个是直接贷款，一个是取钱透支贷款
    :param cardNUM:
    :return:
    '''
    import datetime
    db_manager.make_db(card_num, setting.DB_TYPE)
    credit_account=input("您要贷款多少：")
    db_manager.USER_MSG_DICT[card_num]["exceed"] += credit_account
    #有限日期是当天日志+15天,每次登录查看当前日期是否超过有限日期
    db_manager.USER_MSG_DICT[card_num]["expiration_time"] = str(datetime.datetime.now()+datetime.timedelta(15))
    db_manager.write_to_db(card_num, setting.DB_TYPE)


def using():
    '''
    查看当前用户时谁
    :return:
    '''
    print("当前用户卡号为%s，名字%s"%(NOW_USER["now_card"],
                            db_manager.USER_MSG_DICT[NOW_USER["now_card"]]["name"]))
def interface(cardNUM):
    '''
    此函数提供用户的入口
    :return:
    '''
    menu = '''
    1.登录(login)
    2.注册(register)
    3.存款(deposit)
    4.取款(withdraw)
    5.转账(transfer)
    6.贷款(credit)
    7.登出(logout)
    8.查看当前用户(using)
    exit.退出(exit)
    help.帮助(help)
    '''
    menu_list = {
        "1": login,
        "2": register,
        "3": deposit,
        "4": withdraw,
        "5": transfer,
        "6": credit,
        "7": logout,
        "8": using,
    }
    print(menu)
    while True:
        f_serial = input("user> ")
        if f_serial == "exit":
            return "exit"
        elif f_serial == "help":
            print(menu)
        elif f_serial not in menu_list:
            continue
        elif f_serial == "1" or f_serial == "2" or f_serial == "8":   #当输入1和2时不需要传值
            menu_list[f_serial]()
        else:
            menu_list[f_serial](cardNUM)

        #判断是否全部都登出：如果全部登出返回
        for key in db_manager.USER_MSG_DICT:
            if db_manager.USER_MSG_DICT[key]["loginstatu"] == True:
                break
        else:
            return False

def run():
    '''
    如果要冻结账户，judge返回froze,
    此时先登录
    :return:
    '''
    db_manager.load_file()
    while True:
        frontMenu='''
        1.登录(login)
        2.注册(register)
        exit.退出
        '''
        print(frontMenu)
        f_serial = input(">")
        cardNUM=None
        if f_serial == "1":
            cardNUM, judge = login()
            db_manager.write_to_db(cardNUM, setting.DB_TYPE)
            if judge == "froze":
                froze(cardNUM)
            elif judge:
                f_serial=interface(cardNUM)
            else:
                exit_func()
        elif f_serial == "2":
            register()
        elif f_serial == "exit":
            #退出之前全部登录取消
            exit_func()

def exit_func():
    '''
    此函数专门用于退出,如果是退出消息，返回exit
    :return:
    '''
    for key in db_manager.USER_MSG_DICT:
        db_manager.USER_MSG_DICT[key]["loginstatu"] = False
        db_manager.write_to_db(key, setting.DB_TYPE)
    exit("欢迎再次使用")
