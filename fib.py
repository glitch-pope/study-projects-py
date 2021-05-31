def fib():
    nm = 0
    n = 1
    yield nm
    yield n
    while n < 10 ** 10:
        np = nm + n
        yield np
        nm = n
        n = np

for number in fib():
    print(number)