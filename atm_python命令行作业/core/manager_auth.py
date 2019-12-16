from core import db_manager
from conf import setting
from core.hash_factory import hash_factory
from core import account_factory

M_USER=None
def manager_login():
    '''
    管理员登录接口
    :return:
    '''
    global M_USER

    db_manager.make_db(setting.MANAGER_DB_NAME, setting.DB_TYPE,user_type="manager")
    count = 3
    while True:
        m_user=input("请输入员工姓名：").strip()
        if m_user not in db_manager.MANAGER_MSG_DICT:
            print("%s用户不存在,请重新输入"%m_user)
            continue
        while count > 0:
            m_pwd=input("请输入您的密码：")
            m_pwd=hash_factory(m_pwd)
            if m_pwd == db_manager.MANAGER_MSG_DICT[m_user]:
                print("登录成功")
                '''
                此处加入到管理员日志函数
                '''
                M_USER = m_user
                return True
            else:
                print("登录失败")
                count -= 1
        else:
            exit("登录错误，退出")

def manage_user_login():
    '''
    后台登陆用户
    :return:
    '''
    db_manager.load_file()
    while True:
        card_num = input("请输入用户卡号:")
        db_manager.make_db(card_num, setting.DB_TYPE)
        if card_num.startswith("e"):    #管理员退出登录
            return "exit", False
        elif card_num not in db_manager.USER_MSG_DICT:
            print("用户不存在")
            continue

        IDcard = input("请输入用户身份证:")
        if IDcard == db_manager.USER_MSG_DICT[card_num]["IDcard"]:
            print("%s用户登录成功"%card_num)
            return card_num,True
        elif IDcard == "exit":
            return card_num,False
        else:
            print("该用户身份不匹配")
def unfreeze(card_num):
    '''
    解除冻结
    :param user:
    :return:
    '''
    db_manager.make_db(card_num, setting.DB_TYPE)

    if not db_manager.USER_MSG_DICT[card_num]["userstatu"]:
        db_manager.USER_MSG_DICT[card_num]["userstatu"] = True
        db_manager.USER_MSG_DICT[card_num]["exceed"] = 0
        db_manager.USER_MSG_DICT[card_num]["expiration_time"] = None
        print("%s用户已经解冻"%card_num)
        return True
    else:
        print("%s用户没有被冻结"%card_num)
        return False
def change_user_account(card_num):
    '''
    更改用户余额
    :param user:
    :return:
    '''
    account=db_manager.USER_MSG_DICT[card_num]["account"]
    diff=input("请输入差额:")  #+10,-10
    if diff[0] in ["+","-"]:
        account=account_factory.change_account(int(account),int(diff[1:]),diff[0])
    else:
        account=account_factory.change_account(int(account), int(diff[1:]))
    db_manager.USER_MSG_DICT[card_num]["account"] = str(account)
    print("%s用户的余额还有%s"%(db_manager.USER_MSG_DICT[card_num]["name"],
                         db_manager.USER_MSG_DICT[card_num]["account"]))
    return True
def change_user_message(card_num):
    '''更改用户信息'''
    chg_menu=list(db_manager.USER_MSG_DICT[card_num])
    chg_menu.remove("name")
    print(chg_menu)
    action = input("请输入您的操作")
    print("%s的%s的值为%s"%(db_manager.USER_MSG_DICT[card_num]["name"],action,
                        db_manager.USER_MSG_DICT[card_num][action]))
    if action == "passwd":
        value = input("请输入值")
        value = hash_factory(value)
        db_manager.USER_MSG_DICT[card_num][action] = value
    else:
        value = input("请输入值")
        db_manager.USER_MSG_DICT[card_num][action] = value
    return True

def watch_user_msg(card_num=None,all=False,action=None):
    '''
    管理员查看用户信息
    :param cardNum:
    :param all: True-->查看所有(login(查看已经登录)/froze(查看已经冻结)/all(查看所有))/
    False-->查看cardNum指定的用户
    :return:
    '''
    db_manager.make_db(card_num,setting.DB_TYPE)
    if all == True:
        if action == "login":
            for key in db_manager.USER_MSG_DICT:
                if db_manager.USER_MSG_DICT[key]["loginstatu"] == True:
                    print("卡号:%s，用户%s,已登陆"%(key,db_manager.USER_MSG_DICT[key]["name"]))
        elif action == "froze":
            for key in db_manager.USER_MSG_DICT:
                if db_manager.USER_MSG_DICT[key]["userstatu"] == False:
                    print("卡号:%s，用户%s,已冻结"%(key,db_manager.USER_MSG_DICT[key]["name"]))
        elif action == "all":
            for key in db_manager.USER_MSG_DICT:
                print("卡号:%s，用户%s" % (key, db_manager.USER_MSG_DICT[key]["name"]))
    else:
        print(db_manager.USER_MSG_DICT[card_num])
def watch_log():
    '''

    :return:
    '''
def m_interface(card_num):
    menu='''
    1.解冻用户(unfreeze)
    2.修改用户余额(change_user_account)
    3.修改用户信息(change_user_message)
    4.查看日志(watch_log)
    5.查看用户信息(watch_user_msg)
    help.查看帮助(help)
    exit.退出(help)
    '''
    print(menu)
    menu_dict={
        "1":unfreeze,
        "2":change_user_account,
        "3":change_user_message,
        "4":watch_log
    }
    while True:
        func_serial=input("manager_%s> "%db_manager.USER_MSG_DICT[card_num]["name"])
        if func_serial in menu_dict:
            f_judge=menu_dict[func_serial](card_num)
            if f_judge:
                db_manager.write_to_db(card_num,setting.DB_TYPE)
        elif func_serial ==  "5":
            watch_user_msg(card_num,all=False)
        elif func_serial == "exit":
            return False
        elif func_serial == "help":
            print(menu)
        elif not func_serial:
            continue

def manager_main():
    '''
    管理员主程序
    管理员登录->等待用户->用户登录->用户具体要什么操作（可操作多次）->用户退出->管理员退出
    :return:
    '''
    m_judge = manager_login()
    if m_judge:
        manager_menu='''
        1.查看所有登录的用户
        2.查看所有冻结的用户
        3.查看所有用户
        4.登录用户(manage_user_login)
        5.退出管理(exit)
        '''
        print(manager_menu)
        while True:
            menu_num=input("manager>")
            if not menu_num:
                continue
            elif menu_num == "exit":
                exit("管理端关闭")
            elif menu_num == "1":
                watch_user_msg(action="login", all=True)
            elif menu_num == "2":
                watch_user_msg(action="froze",all=True)
            elif menu_num == "3":
                watch_user_msg(action="all", all=True)
            elif menu_num == "4":
                card_num, judge = manage_user_login()
                if judge:
                    m_interface(card_num)
            elif menu_num == "help":
                print(manager_menu)