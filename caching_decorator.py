from functools import wraps

def caching_decorator(func):
    """
    A decorator that caches the results of a function based on its arguments.
    """
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Create a unique key using args and kwargs
        key = (args, frozenset(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
            print(f"Cache miss for {key}: Calculating result...")
        else:
            print(f"Cache hit for {key}: Using cached result.")
        return cache[key]

    return wrapper

# TESTING THE CACHING DECORATOR
if __name__ == "__main__":
    @caching_decorator
    def expensive_computation(a, b):
        """
        Simulates an expensive computation (e.g., heavy calculation or API call).
        """
        return a ** b + b ** a

    print(expensive_computation(2, 3))  # Cache miss, result calculated
    print(expensive_computation(2, 3))  # Cache hit, result reused
    print(expensive_computation(3, 2))  # Cache miss, result calculated
    print(expensive_computation(2, 3))  # Cache hit, result reused
