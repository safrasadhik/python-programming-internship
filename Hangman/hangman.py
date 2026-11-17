import random

with open("wordlist.txt", "r", encoding="utf-8") as file:
    words = [
        word.strip().upper()
        for word in file
        if word.strip().isalpha()
        and 4 <= len(word.strip()) <= 12
    ]

secret_word = random.choice(words)

print("Word list loaded successfully!")
print("Number of available words:", len(words))

guessed_letters = set()
wrong_guesses = set()
max_attempts = 6

stages = [
    " +---+\n |   |\n     |\n     |\n     |\n=======",
    " +---+\n |   |\n O   |\n     |\n     |\n=======",
    " +---+\n |   |\n O   |\n |   |\n     |\n=======",
    " +---+\n |   |\n O   |\n/|   |\n     |\n=======",
    " +---+\n |   |\n O   |\n/|\\  |\n     |\n=======",
    " +---+\n |   |\n O   |\n/|\\  |\n/    |\n=======",
    " +---+\n |   |\n O   |\n/|\\  |\n/ \\  |\n======="
]

def display_word():
    return " ".join(
        letter if letter in guessed_letters else "_"
        for letter in secret_word
    )

print("\nWelcome to Hangman!")

while len(wrong_guesses) < max_attempts:
    print(stages[len(wrong_guesses)])
    print("\nWord:", display_word())
    print("Guessed letters:", sorted(guessed_letters | wrong_guesses))
    print("Attempts remaining:", max_attempts - len(wrong_guesses))

    guess = input("Guess a letter: ").strip().upper()

    if len(guess) != 1 or not guess.isalpha():
        print("Enter one letter only.")
        continue

    if guess in guessed_letters or guess in wrong_guesses:
        print("You already guessed that letter!")
        continue

    if guess in secret_word:
        guessed_letters.add(guess)
        print("Correct!")
    else:
        wrong_guesses.add(guess)
        print("Incorrect!")

    if all(letter in guessed_letters for letter in secret_word):
        print("\nWord:", display_word())
        print("Congratulations! You won!")
        break
else:
    print(stages[max_attempts])
    print("\nGame over!")
    print("The secret word was:", secret_word)