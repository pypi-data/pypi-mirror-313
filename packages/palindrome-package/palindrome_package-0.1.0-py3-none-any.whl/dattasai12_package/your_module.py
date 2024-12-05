# your_module.py
def is_palindrome(number):
    """
    Check if a given number is a palindrome.
    """
    num_str = str(number)
    return num_str == num_str[::-1]
