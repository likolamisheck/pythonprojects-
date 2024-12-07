import functools
def memoize(max_cache_size=5):
    cache = {}

    def decorator(func):
        def wrapper(*args):
            if args in cache:
                print(f"Fetching from cache for {args}")
                return cache[args]
            else:
                print(f"Calculating result for {args}")
                result = func(*args)
                if len(cache) >= max_cache_size:
                    # Remove the oldest item from the cache
                    oldest_key = next(iter(cache))
                    cache.pop(oldest_key)
                    print(f"Cache full. Removed oldest entry: {oldest_key}")
                cache[args] = result
                return result
        return wrapper
    return decorator

@memoize(max_cache_size=3)
def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

@memoize(max_cache_size=3)
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Example usage
print(factorial(5))  # Should calculate and cache the result
print(factorial(5))  # Should fetch from cache

print(is_prime(11))   # Should calculate and cache the result
print(is_prime(11))   # Should fetch from cache
print(is_prime(4))    # Should calculate and cache the result
print(is_prime(4))    # Should fetch from cache
print(is_prime(13))   # Should calculate and cache the result
print(is_prime(13))   # Should fetch from cache
print(is_prime(15))   # Should calculate and cache the result
print(is_prime(15))   # Should fetch from cache
