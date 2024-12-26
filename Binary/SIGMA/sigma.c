#include <stdio.h>
#include <string.h>

void generate_flag(int user_input) {
    if (user_input == 5362) { // Hidden condition
        // Dynamically construct the flag
        char part1[] = "i-CES{Y0u_";
        char part2[] = "h4vE_6reat_";
        char part3[] = "516m4_CON6R4T5}";
        
        char flag[50];
        snprintf(flag, sizeof(flag), "%s%s%s", part1, part2, part3);

        printf("Congratulations! You've unlocked the hidden flag: %s\n", flag);
    } else {
        printf("Nothing special here. Better luck next time!\n");
    }
}

int main() {
    int sigma_rating;

    printf("Welcome to the Sigma Rating Program!\n");
    printf("Rate your Sigma mindset from 1 to 10: ");
    scanf("%d", &sigma_rating);

    if(sigma_rating == 5362){
        generate_flag(sigma_rating);
    }
    else if (sigma_rating >= 1 && sigma_rating <= 10) {
        printf("\nThank you for rating your Sigma mindset!\n");
        printf("Check out this video: https://www.youtube.com/watch?v=1k6y1JvaGyE\n");
    } else {
        printf("Please choose a number between 1 and 10 next time.\n");
    }

    return 0;
}
