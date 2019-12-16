from core.interface import manager
from core import tools
from core.Base_Classes import *
from core import auth

@auth.auth
def manager_interface():
    '''管理员入口'''
    manager.main()
    pass
def student_interface():
    '''学生入口'''
    pass
def teacher_interface():
    '''教师入口'''
    pass

def main():
    interface_dict={
        1:manager_interface,
        2:student_interface,
        3:teacher_interface
    }
    while True:
        func=tools.input_mod(interface_dict)
        if func == "exit":
            break
        else:
            func()