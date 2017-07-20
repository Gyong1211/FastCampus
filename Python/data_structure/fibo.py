def fibo(n):
    if n==0 or n==1:
        return 1
    return fibo(n-2)+fibo(n-1)


if __name__=="__main__":
    for i in range(10):
        print(fibo(i))
