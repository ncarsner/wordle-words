import sys
import random

from .words import word_list


def main(num_words=5):
    used_letters = set()
    selected_words = []

    for word in random.sample(word_list, len(word_list)):
        if not any(letter in used_letters for letter in word):
            selected_words.append(word)
            used_letters.update(word)

        if len(selected_words) == num_words:
            break

    print("Selected words:", selected_words)
    print("Used letters:", "".join(sorted(used_letters)))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            num_words = int(sys.argv[1])
            main(num_words)
        except ValueError:
            print("Error: Please provide a valid number")
            print("Usage: python main.py [number_of_words]")
    else:
        main()
