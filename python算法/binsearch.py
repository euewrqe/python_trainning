def binsearch(li, n):
    left = 0
    right = len(li) - 1

    while left <= right:
        mid = (left + right) // 2
        if li[mid] == n:
            return mid
        elif li[mid] < n:
            right = mid
        elif li[mid] > n:
            left = mid
    return None


def binsearch_recur(li, n, left=0, right=None):
    left = 0
    right = len(li) - 1
    mid = (left + right) // 2

    if li[mid] == n:
        return mid
    elif li[mid] < n:
        binsearch_recur(li, n,left ,mid)
    elif li[mid] > n:
        binsearch_recur(li, n, mid, right)

    if right < left:
        raise Exception("fffff")


print(binsearch_recur([1,2,3,4,5], 3))