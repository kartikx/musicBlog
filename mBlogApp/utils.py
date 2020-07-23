def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_string = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_string