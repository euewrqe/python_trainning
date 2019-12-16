def quicksort(li, left=0, right=None):
    left = 0
    right = len(li)-1
    if left < right:
        mid =parti(li, left, right)

        quicksort(li, left, mid - 1)
        # quicksort(li, mid, right)
def parti(li, left, right):
    tmp = li[left]

    while left < right:
        while left < right and li[right] >= tmp:
            right -= 1

        li[left] = li[right]
        while left < right and li[left] <= tmp:
            left += 1

        li[right] = li[left]

    li[left] = tmp

    return left





import random
li = list(range(5))
random.shuffle(li)
print(li)
quicksort(li)
print(li)