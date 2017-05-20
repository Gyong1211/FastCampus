#
from running_time_decorator import running_time
#import decorator python file

@running_time
def my_sort_function(list_):
    '''Sorts the list by bringing the smallest value
    to the front of the variable list.'''
    print('Unsorted-list : ',list_)
    for n in range(len(list_)):
        if not list_[n]==min(list_[n:]):
            list_.insert(n,list_.pop(list_.index(min(list_[n:]))))
            
            #n_list_min = min(list_[n:])
            #n_list_min_index = list_.index(n_list_min)
            #list_.insert(n,list_pop.(n_list_min_index))

    print('Sorted list : ',list_)
    return(list_)



list2 = [1324,4545,6,765,234,234,6,43,5,23,7,132,123,151,164,143,21,61,412]
list1=set(list2)
list0=list(list1)
result = my_sort_function(list0)
print(result)


