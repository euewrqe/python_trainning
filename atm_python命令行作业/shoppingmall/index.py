#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__:lixiaoyu
# email:euewrqe@gmail.com
# data:2017/1/14
import re
import pprint
from core import main
store_name = None
product_dict = {}
line_space_len = 0  # 后一格的空格数
line_space_len_old = 0  # 前一格的空格数     (前一格长度-后一格长度)/2=退格数
line_space_len_old_li = [0, ]
backspace_count = 0  # 退格数
temp_li = []
# 字典对象池
dict_obj_pool = []
dict_obj_pool_point = -1  # 字典对象池的指针
this_dict_obj = product_dict
# 先存储字典的第零级
dict_obj_pool.append(this_dict_obj)
dict_obj_pool_point += 1
# this_dict_obj=dict_obj_pool[dict_obj_pool_point]  # 就是product_dict={}，当前字典池的对象

# 键池
key_pool = [0, ]


def add_item(pool, point, this, key_pool, line, count=0):
    """
    此函数用于添加字典元素
    :param pool:   池
    :param point:   池的最后一格
    :param this:    池的最后一格的对象
    :param line:    要添加的内容
    :param count:    退格的次数
    :return:
    """
    while count > 0:  # 退格的次数

        pool.pop(point)
        key_pool.pop(point)

        point -= 1
        count -= 1
    # 下一级不退格，同级退一格，上一级推两格，结果发现想法是错的，。退完格后，先赋值给指针this当前最后一格的数据,
    # 指针this拿到数据，做另一个分支的下一格，再把下一格赋值给this，池再加一格。退格不一定，加格一定
    this = pool[point]

    this[line] = {}
    key_pool.append(line)

    this = this[line]
    pool.append(this)
    point += 1
    return pool, point, this


# 读取文件，并写成字典的形式
f = open("super", "r", encoding="utf8")
for line in f.readlines():
    if not line.strip():
        continue
    line_space = re.match("^ +", line)  # group当没有匹配内容的时候，报错
    if not line_space:  # 如果没有空格，说明是顶行，顶行只能是店名
        line = line.strip()
        store_name = line
    else:
        line_space_len = len(line_space.group(0))  # 空格有多少
        backspace_count = abs(int((line_space_len - line_space_len_old_li[-1]) / 4)) + 1
        line_space_len_old_li.append(line_space_len)
        level = int(line_space_len / 4)  # 空格数/4=1第一级,2为第二级
        line = line.strip()
        if level > dict_obj_pool_point:  # 当level数大于字典对象池的级别,直接下一级
            
            dict_obj_pool, dict_obj_pool_point, this_dict_obj = add_item(dict_obj_pool, dict_obj_pool_point,
                                                                         this_dict_obj, key_pool, line, count=0)

        elif level == dict_obj_pool_point:  # 需要返回上一级
            
            dict_obj_pool, dict_obj_pool_point, this_dict_obj = add_item(dict_obj_pool, dict_obj_pool_point,
                                                                         this_dict_obj, key_pool, line, count=1)
            if line_space_len_old_li[-1] == line_space_len_old_li[-2]:
                line_space_len_old_li.pop()

        elif level < dict_obj_pool_point:   # 可以返回n级
            
            dict_obj_pool, dict_obj_pool_point, this_dict_obj = add_item(dict_obj_pool, dict_obj_pool_point,
                                                                         this_dict_obj, key_pool, line,
                                                                         count=backspace_count)
f.close()
## 整理字典

salary = int(input("pls input your salary:"))
choice_li = []


def toBalance():
    """
    结算
    :return
    """
    global salary
    balance_count = 0
    print("您购买的商品有")
    for goods, dollar in choice_li:
        print("%s,价格 \033[32m%s\033[0m" % (goods, dollar))
        balance_count += int(dollar)
    print("总价为%s" % (balance_count))
    flag = input("是否结算[y/n]")
    if flag:
        salary -= balance_count
        print("您还有余额\033[32m%s\033[0m:" % (salary))
        print("再见!!!")
        exit()


on_balance_count = 0
menu_key_li = []


def cleanDict(pro_dict):
    """
    此函数专门有来购买商品，有一些命令可以使用help查看
    :param pro_dict:
    :return:    返回上一层
    """
    global on_balance_count

    num = None
    while True:
        menu_key_li.clear()
        for i, k in enumerate(pro_dict):      # 打印商品，一边打印一边保存键
            print("%s. %s" % (i, k))
            menu_key_li.append(k)

        num = input("pls input num：")
        if num.isdigit():
            num = int(num)
            if num >= 0 and num < len(menu_key_li):    # 
                if re.match("^- +(.*) +& +([0-9]+)", menu_key_li[num]):
                    split_temp = re.split("^- +(.*) +& +([0-9]+)", menu_key_li[num])
                    split_temp[2] = int(split_temp[2])
                    if on_balance_count + split_temp[2] > salary:
                        print("您购买的商品，超过您的余额\033[32m%s\033[0m,无法购买" % (salary - on_balance_count - split_temp[2]))
                    else:
                        on_balance_count += split_temp[2]
                        choice_li.append((split_temp[1], split_temp[2]))
                        print("<%s>,价格\033[31m%s\033[0m" % (split_temp[1], split_temp[2]))
                elif not pro_dict[menu_key_li[num]]:
                    print("%s没有货" % menu_key_li[num])
                    menu_key_li.clear()
                else:
                    cleanDict(pro_dict[menu_key_li[num]])
            else:
                print("你输入的代号，没有此商品")
        elif num == "exit":
            return
        elif num == "carry":
            toBalance()
        elif num == "help":
            print('''
            您可以选择：
            商品代号：购买商品
            \033[32mexit\033[0m:返回上一级菜单
            \033[32mcarry\033[0m:结账
            \033[32mlist\033[0m:列出购物车内的商品
            \033[32mdel\033[0m:删除购买的商品
            ''')
        elif num == "list":
            for goods, dollar in choice_li:
                print("%s,价格 \033[32m%s\033[0m" % (goods, dollar))
        elif num == "del":
            for i, goods in enumerate(choice_li):
                print("%s. %s,价格 \033[32m%s\033[0m" % (i, goods[0], goods[1]))
            seq = int(input("pls input your choice"))
            if seq >= 0 and seq < len(choice_li):
                print("您删除了%s:\033[32m%s\033[0m" % (choice_li[seq][0], choice_li[seq][1]))
                on_balance_count -= int(choice_li[seq][1])
                print("您还剩余额有%s" % (salary - on_balance_count))
                choice_li.pop(seq)
            else:
                print("您没有购买此标号的物品")


cleanDict(product_dict)
