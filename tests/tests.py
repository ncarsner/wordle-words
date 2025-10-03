from src.words import word_list


def test_all_words_five_letters():
    assert all(len(word) == 5 for word in word_list)


def test_no_duplicate_words():
    assert len(word_list) == len(set(word_list))


def test_word_list_alphabetical():
    assert word_list == sorted(word_list)
