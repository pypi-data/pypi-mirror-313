from functools import cmp_to_key

def compare_dicts(a, b):
    """Compare two dictionaries based on the 'value' key."""
    if a['value'] < b['value']:
        return -1
    elif a['value'] > b['value']:
        return 1
    else:
        return 0

def custom_sort_dicts(data):
    """Sort a list of dictionaries based on the 'value' key."""
    return sorted(data, key=cmp_to_key(compare_dicts))

def fibonacci(n, memo={}):
    """Calculate the nth Fibonacci number using memoization."""
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci(n-1, memo) + fibonacci(n-2, memo)
    return memo[n]

def is_palindrome(s):
    """Check if a string is a palindrome."""
    return s == s[::-1]
