def binary_search(data, target):
    data.sort()
    start = 0
    end = len(data)-1
    i=0

    while start<=end:
        i+=1
        mid = (end+start)//2
        print(start, data[mid], end)
        if data[mid]==target:
            print(target)
            return
        if data[mid] > target:
            end = mid-1
        else:
            start = mid+1
    return print('못찾았따')

if __name__ == "__main__":
    _list = [i for i in range(4,15)]
    print(_list)
    binary_search(_list, 1)
