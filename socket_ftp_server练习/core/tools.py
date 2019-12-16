#!/usr/bin/env python
#--coding: utf-8--
import sys,os
if os.name == "posix":
    show_color=True
else:
    show_color=False

def make_color(msg,color="red",fillchar="",width=0,output=True,show_color=show_color):
    '''更改字体颜色，默认红色,并设置左右填充'''
    if not show_color:
        # 在windows上不加颜色代码
        if output:
            print(msg)
        return msg
    color_menu={
        "red":"\033[0;31m%s\033[0m",
        "green":"\033[0;32m%s\033[0m",
        "yellow":"\033[0;33m%s\033[0m",
        "blue":"\033[0;34m%s\033[0m",
        "purple":"\033[0;35m%s\033[0m",
        "cyan":"\033[0;36m%s\033[0m",
    }
    if fillchar:
        msg=color_menu[color]%(msg.center(width,fillchar))
    else:
        msg=color_menu[color]%(msg)

    if output:
        print(msg)
    return msg


def view_bar(num, total=100,ratesize=50,rate_format="%d%%[%s%s]"):
    '''
    进度条工具
    :param num:  当前位置
    :param total:   范围
    :return:
    '''
    rate_num = num*(ratesize/total)
    rate_format="\r%s"%rate_format
    r = rate_format % (num,"=" * int(rate_num), " " * (ratesize-int(rate_num)))
    print(r,end="")


def unit_change(byte,unit="M"):
    '''单位换算工具'''
    if unit.upper() == "B":
        byte = byte
    elif unit.upper() == "K":
        byte = byte/1024
    elif unit.upper() == "M":
        byte = byte/1024 / 1024
    elif unit.upper() == "G":
        byte = byte / 1024 / 1024 /1024
    elif unit.upper() == "T":
        byte = byte / 1024 / 1024 /1024/1024
    return byte
