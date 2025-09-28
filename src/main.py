from random import shuffle

from words import words


def main(num_words=5):
    shuffle(words)
    used_letters = set()
    selected_words = []

    for word in words:
        if not any(letter in used_letters for letter in word):
            selected_words.append(word)
            used_letters.update(word)

        if len(selected_words) == num_words:
            break

    print("Selected words:", selected_words)
    print("Used letters:", used_letters)


if __name__ == "__main__":
    main()
