import random

def bubblesort(list_):
    for i in range(len(list_)):
        print(i,'번째 패스')
        for j in range(len(list_)-i-1):
            if list_[j]>list_[j+1]:
                list_[j],list_[j+1] = list_[j+1],list_[j]
                print(list_)
            else:
                print(list_)
    return list_

list1 = list(range(10))
random.shuffle(list1)
print(list1)
result = bubblesort(list1)
print(result)
