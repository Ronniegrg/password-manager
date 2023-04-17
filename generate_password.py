import random
import string


def generate_password(length):
    # Generates a random password of given length
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password
