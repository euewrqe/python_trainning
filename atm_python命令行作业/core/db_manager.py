import json
from conf import setting
import glob
import os
# 卡号组
CARD_GROUP=[]
USER_MSG_DICT={}
MANAGER_MSG_DICT={}
def load_file():
    '''load_db_file to card_group'''
    file_path=os.path.join(setting.BASE_DIR,"db",setting.DB_NAME)
    CARD_GROUP.extend(map(lambda x:os.path.splitext(x)[0],glob.glob1(file_path,"*")))
    #内容得到的是xxx.json，去掉json，只留xxx

def make_db(db_user,db_type=setting.DB_TYPE,user_type = "user"):
    '''
    创建用户字典
    :param db_name:
    :param db_type:
    :param user_type:
    :return:
    '''
    if user_type == "user":
        file_path=os.path.join(setting.BASE_DIR,"db",setting.DB_NAME,"%s.json"%db_user)
        if glob.glob(file_path):
            if db_type == setting.DB_TYPE:
                with open(file_path,"r",encoding="utf-8") as f:
                    USER_MSG_DICT.clear()
                    USER_MSG_DICT.update(json.loads(f.read()))
            else:
                exit("%s,该路径找不到文件"%file_path)
    elif user_type == "manager":
        file_path = os.path.join(setting.BASE_DIR, "db", "%s.json" % setting.MANAGER_DB_NAME)
        if glob.glob(file_path):
            if db_type == setting.DB_TYPE:
                with open(file_path,"r",encoding="utf-8") as f:
                    MANAGER_MSG_DICT.clear()
                    MANAGER_MSG_DICT.update(json.loads(f.read()))
            else:
                exit("%s,该路径找不到文件"%file_path)

def write_to_db(db_user,db_type=setting.DB_TYPE,user_type = "user",create=False):
    '''
    保存用户字典
    :param db_name:
    :param db_type:
    :param user_type:
    :return:
    '''
    if user_type == "user":
        file_path = os.path.join(setting.BASE_DIR, "db",setting.DB_NAME, "%s.json" % db_user)
        if db_type == setting.DB_TYPE:
            with open(file_path,"w",encoding="gbk") as f:
                json.dump(USER_MSG_DICT,f)
    elif user_type == "manager":
        file_path = os.path.join(setting.BASE_DIR, "db", "%s.json" % setting.MANAGER_DB_NAME)
        if db_type == setting.DB_TYPE:
            with open(file_path,"w",encoding="gbk") as f:
                json.dump(MANAGER_MSG_DICT,f)
