#!/usr/bin/env python
#--coding:utf-8--
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import easygui
result=easygui.multenterbox(title="login", fields=("name","birth"))
print(result)
result=easygui.boolbox("真红专题",title="五彩斑斓的世界",choices=("我要真红","我要青空"),
                image="zhenghong.gif")
if result:
    result=easygui.buttonbox(title="真红大法好",image="zh01.gif",choices=("舔一口","撸一管","留言"))
    if result=="舔一口":
        result=easygui.choicebox("你要舔哪里",choices=("脸","头发","脚"))
        easygui.msgbox("你个变态，给我滚",image="huaji.gif")
    elif result=="撸一管":
        easygui.multchoicebox("请选择你用哪只手","开始无节操撸管",("左手","右手"))
    elif result=="留言":
        pwd=easygui.passwordbox()
        if pwd=="123456":
            easygui.textbox("留言区","请给真红留言")
        else:
            easygui.msgbox("密码错误")

#文件写入打开保存

#指定目录
result=easygui.diropenbox()
print(result)
#文件打开
result=easygui.fileopenbox(filetypes=["*.txt", ])
read_msg=""
if result:
    with open(result,encoding="utf-8") as fp:
        read_msg=fp.read()

#写入内容
input_msg=easygui.textbox(text=read_msg)

#保存文件
result=easygui.filesavebox()
print(result)
if result:
    with open(result,"w", encoding="utf-8") as fp:
        fp.write(input_msg)

