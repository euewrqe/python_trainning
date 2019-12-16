def change_account(account,diff_res,sign="+"):
    if sign == "+":
        account += diff_res
    elif sign == "-":
        account -= diff_res
    return account

from conf import setting
def user_change_account(db_manager,cardNUM,action):
    '''

    :param db_manager:
    :param cardNUM:
    :param action: deposit/withdraw
    :return:
    '''
    db_manager.make_db(setting.DB_NAME,setting.DB_TYPE)
    if action == "deposit":
        diff_res=int(input("您要存多少："))
        account=db_manager.USER_MSG_DICT[cardNUM]["account"]
        change_account(account,diff_res,sign="+")
    elif action == "withdraw":
        diff_res = int(input("您要存多少："))
        account = db_manager.USER_MSG_DICT[cardNUM]["account"]
        change_account(account, diff_res, sign="+")
    db_manager.write_to_db(setting.DB_NAME,setting.DB_TYPE)
    return True
