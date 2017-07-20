def binary_search(data, target, start=None, end=None):
    if not start:
        start = 0
    if not end:
        end = len(data)-1
    print('start: {}, end: {}'.format(start,end))

    if start<=end:
        mid = (end+start)//2
        if data[mid]==target:
            print('찾았다')
            print(target)
            print('끝')
            return
        elif data[mid] > target:
            binary_search(data, target, start, mid-1)
        elif data[mid] < target:
            binary_search(data, target, mid+1, end)
    else:
       return print('못찾았따')

if __name__ == "__main__":
    _list = [i for i in range(1,15)]
    print(_list)
    binary_search(_list, 17)
    
