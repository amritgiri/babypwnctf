import hashlib
import sys

# Secret constant number
SECRET_NUMBER = 33700
SECRET_HASH = hashlib.sha256(str(SECRET_NUMBER).encode()).hexdigest()

def hash_input(input_number):
    """Hashes the input number using SHA-256 and returns the hexadecimal digest."""
    return hashlib.sha256(str(input_number).encode()).hexdigest()

def check_guess(user_guess):
    """Checks if the hashed guess matches the secret hash."""
    guessed_hash = hash_input(user_guess)
    return guessed_hash == SECRET_HASH

def main():
    print("Welcome to the Guess the Number Challenge!")
    print("Guess the secret number!")

    # print(f"Hint: The hash of the secret number is: {SECRET_HASH}")

    while True:
        try:
            user_input = int(input("Enter your guess: ").strip())
            if 1 <= user_input <= 40000:
                if check_guess(user_input):
                    print(f"Congratulations! You guessed it right. The secret number was {SECRET_NUMBER}.")
                    print("The flag is: i-CES{9UE5S3d_C0Ns74Nt_H4SH3d_NUm63R}")
                    break
                else:
                    print("https://www.youtube.com/watch?v=1k6y1JvaGyE")
                    sys.exit()
            else:
                print("Please enter a number between 1 and 100.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    main()
