def bubblesort(list_):
    length = len(list_)
    for x in range(length-1,0,-1):
        print('--------------------')
        for y in range(x):
            a, b = list_[y], list_[y+1]
            if a>b:
                list_[y], list_[y+1] = b, a
            print(y+1)
            print(list_)
    return list_

if __name__ == "__main__":
    bubblesort([4,6,2,6,8,9,1])
