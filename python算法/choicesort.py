def choicesort(li):
    for i in range(len(li)):   #n
        min = i
        for j in range(i+1, len(li)): #n-i  n(n-i)
            if li[j] < li[min]:
                min = j
        li[i], li[min] = li[min], li[i]
import random
li = list(range(1000))
random.shuffle(li)
print(li)
choicesort(li)
print(li)


