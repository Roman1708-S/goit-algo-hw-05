def caching_fibonacci():
    """
    Створює та повертає функцію fibonacci(n), яка обчислює n-те число
    Фібоначчі з використанням кешування (мемоізації) через замикання.
    """
    cache = {}

    def fibonacci(n):
        if n <= 0:
            return 0
        if n == 1:
            return 1
        if n in cache:
            return cache[n]
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci


if __name__ == "__main__":
    fib = caching_fibonacci()
    print(fib(10))  # 55
    print(fib(15))  # 610
    print(fib(20))  # 6765