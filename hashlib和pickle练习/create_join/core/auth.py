import json,os
from conf import setting
from core import tools

def auth(func):
    def login(*args,**kwargs):
        print(tools.make_color("登录窗口", color="yellow"))
        user_dict={}
        manager_path=os.path.join(setting.DB_DIR,"manager.json")
        with open(manager_path,"r",encoding="utf8") as f:
            user_dict=json.load(f)
        name = input('请输入用户名: ').strip()
        pas = input('请输入密码: ').strip()
        if user_dict["user"] == name and user_dict["password"] == pas:
            print(tools.make_color("登录成功",color="green"))
            temp_data=func(*args,**kwargs)
            return temp_data
        else:
            print("帐号密码输入错误")

    #让login的文档显示实际函数的文档
    login.__doc__ = func.__doc__
    return login