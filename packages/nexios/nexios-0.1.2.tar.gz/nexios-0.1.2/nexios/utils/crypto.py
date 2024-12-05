import random
import string

def generate_random_string(length, allowed_characters=None):
    if allowed_characters is None:
        allowed_characters = string.ascii_letters + string.digits + string.punctuation
    
    random_string = ''.join(random.choice(allowed_characters) for _ in range(length))
    return random_string
