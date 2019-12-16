'''
该脚本存放一些通用的函数
'''
def make_color(msg,color="red",fillchar="",width=0):
    '''更改字体颜色，默认红色,并设置左右填充'''
    color_menu={
        "red":"\033[0;31m%s\033[0m",
        "green":"\033[0;32m%s\033[0m",
        "yellow":"\033[0;33m%s\033[0m",
        "blue":"\033[0;34m%s\033[0m",
        "purple":"\033[0;35m%s\033[0m",
        "cyan":"\033[0;36m%s\033[0m",
    }
    if fillchar:
        return color_menu[color]%(msg.center(width,fillchar))
    else:
        return color_menu[color]%(msg)

def print_menu(menu,title="鲁迅资源站"):
    print(make_color(title,"red","*",40))
    for num in menu:
        print(num,menu[num].__doc__ if menu[num].__doc__ else menu[num].__name__)


def input_mod(temp_dict,title="鲁迅资源站"):
    print_menu(temp_dict,title)
    while True:
        num = input("pls input your choice")
        if not num:
            continue
        elif num == "exit":
            return "exit"
        elif int(num) not in temp_dict:
            print(make_color("该数字不存在"))
        else:
            num=int(num)
            return temp_dict[num]
