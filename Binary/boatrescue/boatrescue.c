#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/sha.h>

// Secret constant number
#define SECRET_NUMBER 33700

void sha256_hash(const char *str, char outputBuffer[65]) {
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256_CTX sha256;

    // Initialize, update and finalize hash with new OpenSSL API
    SHA256_Init(&sha256);
    SHA256_Update(&sha256, str, strlen(str));
    SHA256_Final(hash, &sha256);

    for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
        sprintf(outputBuffer + (i * 2), "%02x", hash[i]);
    }
    outputBuffer[64] = 0;
}

int main() {
    char secret_hash[65];
    char input_hash[65];
    char input_str[10];

    // Compute the hash of the secret number
    snprintf(input_str, sizeof(input_str), "%d", SECRET_NUMBER);
    sha256_hash(input_str, secret_hash);

    printf("Welcome to the Guess the Number Challenge!\n");
    printf("Guess the secret number!\n");

    while (1) {
        int user_input;
        printf("Enter your guess: ");
        if (scanf("%d", &user_input) != 1 || user_input < 1 || user_input > 40000) {
            printf("Please enter a valid number between 1 and 40000.\n");
            // Clear the input buffer
            while (getchar() != '\n');
            continue;
        }

        // Hash the user's input
        snprintf(input_str, sizeof(input_str), "%d", user_input);
        sha256_hash(input_str, input_hash);

        // Compare hashes
        if (strcmp(input_hash, secret_hash) == 0) {
            char flag[50];
            snprintf(flag, sizeof(flag), "i-CES{%s}", "9UE5S3d_C0Ns74Nt_H4SH3d_NUm63R");
            printf("Congratulations! You guessed it right. The secret number was %d.\n", SECRET_NUMBER);
            printf("The flag is: %s\n", flag);
            break;
        } else {
            printf("https://www.youtube.com/watch?v=1k6y1JvaGyE\n");
            exit(0);
        }
    }

    return 0;
}
