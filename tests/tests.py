from words import words

def test_duplicate_words():
    assert len(words) != len(set(words))

def test_word_list_alphabetical():
    assert words == sorted(words)

def test_basic():
    assert 1 + 1 == 2