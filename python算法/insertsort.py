
'''
    05 1 45648912
    015 4 5648912
    0145 5 648912
    01455 6 48912
    014556 4 8912
    0144556 8 912
    01445568 9 12
    014455689 1 2
    0114455689 2
    01124455689


'''
def insertsort(li):
    for i in range(2, len(li)-1):

        tmp = li[2]
        insert(li, tmp, i-1)

#从后往前找，比tmp大的，指针就往前移动，并数组元素往后移动一格
def insert(li, tmp, length):
    while tmp < li[length]:
        li[length + 1] = li[length]
        length -= 1

    li[length] = tmp






import random
li = [0,5,1,4,5,6,4,8,9,1,2, 0]
insertsort(li[-1])
print(li)