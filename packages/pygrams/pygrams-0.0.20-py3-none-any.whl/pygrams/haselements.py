def has_armstrong(list_of_numbers):
    """
    Checks if the list has at least one Armstrong number.

    An Armstrong number is a number that is equal to the sum of its digits raised
    to the power of the number of digits.
    
    :param list_of_numbers: list - List of numbers.
    :return: bool - True if at least one Armstrong number exists, False otherwise.
    """
    for number in list_of_numbers:
        total = 0
        digits = str(number)
        num_digits = len(digits)
        
        for digit in digits:
            total += int(digit) ** num_digits
        
        if total == number:
            return True
    
    return False


def has_even_number(numbers):
    """
    Checks if a list contains at least one even number.

    :param numbers: list - List of integers.
    :return: bool - True if an even number exists, False otherwise.
    """
    for number in numbers:
        if number % 2 == 0:
            return True
    return False


def has_odd_number(numbers):
    """
    Checks if a list contains at least one odd number.

    :param numbers: list - List of integers.
    :return: bool - True if an odd number exists, False otherwise.
    """
    for number in numbers:
        if number % 2 != 0:
            return True
    return False


def has_prime_number(numbers):
    """
    Checks if a list contains at least one prime number.

    :param numbers: list - List of integers.
    :return: bool - True if a prime number exists, False otherwise.
    """
    for number in numbers:
        if number > 1:  # Prime numbers are greater than 1
            is_prime = True
            for i in range(2, int(number**0.5) + 1):  # Check divisors up to sqrt(number)
                if number % i == 0:
                    is_prime = False
                    break
            if is_prime:
                return True
    return False


def has_capital_letter(a_string):
    """
    Checks if the string contains at least one uppercase letter.
    
    :param a_string: str - The string to check.
    :return: bool - True if there's at least one uppercase letter, False otherwise.
    """
    for letter in a_string:
        if letter.isupper():
            return True
    return False


def has_small_letter(a_string):
    """
    Checks if the string contains at least one lowercase letter.
    
    :param a_string: str - The string to check.
    :return: bool - True if there's at least one lowercase letter, False otherwise.
    """
    for letter in a_string:
        if letter.islower():
            return True
    return False


def has_underscore(a_string):
    """
    Checks if the string contains an underscore (_).
    
    :param a_string: str - The string to check.
    :return: bool - True if there's an underscore, False otherwise.
    """
    return "_" in a_string


def has_white_space(a_string):
    """
    Checks if the string contains a white space ( ).
    
    :param a_string: str - The string to check.
    :return: bool - True if there's a white space, False otherwise.
    """
    return " " in a_string


def has_period(a_string):
    """
    Checks if the string contains a period (.).
    
    :param a_string: str - The string to check.
    :return: bool - True if there's a period, False otherwise.
    """
    return "." in a_string


def has_colon(a_string):
    """
    Checks if the string contains a colon (:).
    
    :param a_string: str - The string to check.
    :return: bool - True if there's a colon, False otherwise.
    """
    return ":" in a_string


def has_semi_colon(a_string):
    """
    Checks if the string contains a semicolon (;).
    
    :param a_string: str - The string to check.
    :return: bool - True if there's a semicolon, False otherwise.
    """
    return ";" in a_string


def has_comma(a_string):
    """
    Checks if the string contains a comma (,).
    
    :param a_string: str - The string to check.
    :return: bool - True if there's a comma, False otherwise.
    """
    return "," in a_string


def has_operator(a_string):
    """
    Checks if the string contains any of the operators (+, -, *, /, %).
    
    :param a_string: str - The string to check.
    :return: bool - True if any operator exists, False otherwise.
    """
    operators = ["+", "-", "*", "/", "%"]
    for operator in operators:
        if operator in a_string:
            return True
    return False


def has_number(a_string):
    """
    Checks if the string contains a number (digit).
    
    :param a_string: str - The string to check.
    :return: bool - True if there's at least one digit, False otherwise.
    """
    for letter in a_string:
        if letter.isdigit():
            return True
    return False


def has_symbol(a_string):
    """
    Checks if the string contains any special symbol (e.g., @, #, $, etc.).
    
    :param a_string: str - The string to check.
    :return: bool - True if any special symbol exists, False otherwise.
    """
    symbols = ["@", "#", "$", "%", "^", "&", "*", "(", ")", "<", ">", "?", "/", "\\", "|", "}", "{", "~", ":", "'", "\""]
    for symbol in symbols:
        if symbol in a_string:
            return True
    return False


def has_element(string, element):
    """
    Checks if the string contains the specified element.
    
    :param string: str - The string to check.
    :param element: str - The element to check for.
    :return: bool - True if the element is found, False otherwise.
    """
    return element in string
