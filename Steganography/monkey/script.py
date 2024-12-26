import os
import base64
import random
import string

def generate_random_base64(length=64):
    """Generate a random base64 string of the given length."""
    random_bytes = os.urandom(length)
    return base64.b64encode(random_bytes).decode()

def generate_random_filename(length=8):
    """Generate a random alphanumeric filename of the given length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_base64_files(num_files=50):
    """Generate random base64 files with random filenames."""
    for _ in range(num_files):
        base64_string = generate_random_base64()
        filename = generate_random_filename()
        with open(filename, 'w') as file:
            file.write(base64_string)
        print(f'Generated {filename}')

# Generate 50 random base64 files with random names
generate_base64_files()
