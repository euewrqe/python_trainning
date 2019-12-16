def pupple_sort(li):
    for i in range(len(li)):
        # i个数已经交换完的
        for j in range(len(li)-1-i):
            if li[j] > li[j+1]:
                tmp = li[j]
                li[j] = li[j+1]
                li[j+1] = tmp


import random
li = [random.randrange(1,9) for i in range(10)]
print(li)
pupple_sort(li)
print(li)