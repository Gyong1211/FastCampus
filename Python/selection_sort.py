import random

def selection_sort(list_):
    ll = len(list_) #리스트의 길이
    for i in range(ll-1):
        min_val = list_[i]
        min_idx = i
        print(str(i+1)+'번째 요소 비교 중')
        for j in range(i+1,ll):
            if min_val<list_[j]:
                #print(list_,'올바른 자리 현재 최소값:'+str(min_val))
                pass
            else:
                min_val=list_[j]
                min_idx=j
                print(list_,str(i+1)+'번째 요소보다 '+str(j+1)+'번째 요소가 작음')
        list_[min_idx], list_[i] = list_[i], list_[min_idx]
        #list_[min_idx]=list_[i]
        #list_[i]=min_val
        print(list_, str(i+1)+'번째 요소 정렬 완료')
    print('정렬 완료')
    print(list_)
    return(list_)


list1 = list(range(0,10))
random.shuffle(list1)
print(list1)
selection_sort(list1)

