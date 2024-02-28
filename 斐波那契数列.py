def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    else:
        fib_list = [0, 1]
        while len(fib_list) < n:
            new_num = fib_list[-1] + fib_list[-2]
            fib_list.append(new_num)
        return fib_list

