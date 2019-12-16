'''
该文件用于修改配置
DB_TYPE ---指定数据库类型,可选择json或者sqlite
DB_NAME ---指定数据库名
'''
import os
import logging
# 根目录位置
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DB_TYPE_LI = ["json", "sqlite"]
DB_TYPE = "json"
DB_NAME = "user_db"

MANAGER_DB_NAME="manager"

USER_PASS_LEN = 6
CARD_ID_LEN = 6
CARD_NUM_ID = 6

# 是否打印至屏幕
STREAM_HD = True
FILE_HD = True

STREAM_FORMAT="%(asctime)s %(filename)s %(levelname)s %(message)s"
FILE_FORMAT="%(asctime)s %(filename)s %(levelname)s %(message)s"


DATE_FORMAT = "%Y/%m/%d %H:%M:%S"

LOG_LEVEL=logging.DEBUG
LOG_TYPE={
    "user_log":"user.log",
    "manager_log":"manager.log",
}
