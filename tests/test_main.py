import pytest
from unittest.mock import MagicMock

from src.wordle_manager.main import main
from src.wordle_manager.utils import WordListManager, has_repeating_letters
from src.wordle_manager import words


@pytest.fixture(autouse=True)
def safe_testing_environment():
    """Fixture to prevent any file writes and preserve original word list"""
    original_words = words.word_list.copy()
    original_id = id(words.word_list)

    with pytest.MonkeyPatch.context() as monkeypatch:
        monkeypatch.setattr(
            WordListManager, "save_to_file", lambda *args, **kwargs: None
        )
        try:
            yield
        finally:
            if id(words.word_list) != original_id:
                words.word_list = original_words
            else:
                words.word_list[:] = original_words


@pytest.fixture
def mock_word_list_manager():
    mock_manager = MagicMock()
    return mock_manager


@pytest.fixture
def mock_parse_args():
    mock_args = MagicMock()
    return mock_args


@pytest.mark.parametrize(
    "sys_argv, expected_action, setup_mocks, verify_calls",
    [
        pytest.param(
            ["script_name", "5"],
            "run",
            lambda: None,  # No additional setup needed
            lambda mock_run, mock_manager: mock_run.assert_called_once_with(5, unique_letters=False),
            id="run_with_number"
        ),
        pytest.param(
            ["script_name", "stats"],
            "stats",
            lambda: MagicMock(action="stats"),
            lambda mock_run, mock_manager: mock_manager.show_stats.assert_called_once(),
            id="stats_action",
        ),
        pytest.param(
            ["script_name", "find-scarce", "--num", "5"],
            "find-scarce",
            lambda: MagicMock(action="find-scarce", num=5),
            lambda mock_run,
            mock_manager: mock_manager.find_scarce_letters.assert_called_once_with(5),
            id="find_scarce_action",
        ),
        pytest.param(
            ["script_name", "dedup"],
            "dedup",
            lambda: MagicMock(action="dedup"),
            lambda mock_run,
            mock_manager: mock_manager.remove_duplicates.assert_called_once(),
            id="dedup_action",
        ),
        pytest.param(
            ["script_name", "sort"],
            "sort",
            lambda: MagicMock(action="sort"),
            lambda mock_run, mock_manager: mock_manager.sort_words.assert_called_once(),
            id="sort_action",
        ),
        pytest.param(
            ["script_name", "add", "newword"],
            "add",
            lambda: MagicMock(action="add", word="newword"),
            lambda mock_run,
            mock_manager: mock_manager.add_word.assert_called_once_with("newword"),
            id="add_action",
        ),
    ],
)
def test_main_actions(
    sys_argv, expected_action, setup_mocks, verify_calls, monkeypatch
):
    mock_word_list_manager = MagicMock()
    mock_run = MagicMock()

    # Mock the parse_args function if it's not a "run" action
    if expected_action != "run":
        mock_parse_args_result = setup_mocks()
        monkeypatch.setattr(
            "src.wordle_manager.main.parse_args", lambda: mock_parse_args_result
        )
        monkeypatch.setattr(
            "src.wordle_manager.main.WordListManager", lambda: mock_word_list_manager
        )
    else:
        # For "run" action, mock the run function
        monkeypatch.setattr("src.wordle_manager.main.run", mock_run)

    monkeypatch.setattr("sys.argv", sys_argv)

    # All actions now just return (no SystemExit)
    main()

    verify_calls(mock_run, mock_word_list_manager)


def test_main_add_action_no_word_exits_with_error(mock_parse_args, capsys, monkeypatch):
    mock_parse_args.action = "add"
    mock_parse_args.word = None
    monkeypatch.setattr("src.wordle_manager.main.parse_args", lambda: mock_parse_args)
    # Ensure sys.argv doesn't trigger the run() branch
    monkeypatch.setattr("sys.argv", ["script", "add"])

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1

    captured = capsys.readouterr()
    assert "Error: No word provided to add." in captured.out


def test_main_clean_action(
    mock_word_list_manager, mock_parse_args, capsys, monkeypatch
):
    mock_parse_args.action = "clean"
    monkeypatch.setattr("src.wordle_manager.main.parse_args", lambda: mock_parse_args)
    monkeypatch.setattr(
        "src.wordle_manager.main.WordListManager", lambda: mock_word_list_manager
    )
    # Ensure sys.argv doesn't trigger the run() branch
    monkeypatch.setattr("sys.argv", ["script", "clean"])

    main()

    mock_word_list_manager.remove_invalid_words.assert_called_once()

    captured = capsys.readouterr()
    assert "Clean operation completed" in captured.out


def test_main_unknown_action_with_non_numeric_word_arg(mock_parse_args, monkeypatch):
    mock_parse_args.action = "unknown"
    mock_parse_args.word = "notanumber"
    monkeypatch.setattr("src.wordle_manager.main.parse_args", lambda: mock_parse_args)
    # Ensure sys.argv doesn't trigger the run() branch
    monkeypatch.setattr("sys.argv", ["script", "unknown", "notanumber"])

    main()


def test_main_unique_letters_flag(monkeypatch):
    mock_run = MagicMock()
    monkeypatch.setattr("src.wordle_manager.main.run", mock_run)
    monkeypatch.setattr("sys.argv", ["script_name", "-u"])

    main()

    mock_run.assert_called_once_with(3, unique_letters=True)

def test_main_numeric_arg_with_unique_letters_flag(monkeypatch):
    mock_run = MagicMock()
    monkeypatch.setattr("src.wordle_manager.main.run", mock_run)
    monkeypatch.setattr("sys.argv", ["script_name", "2", "-u"])

    main()

    mock_run.assert_called_once_with(2, unique_letters=True)

@pytest.mark.parametrize("word, expected", [
    ("spill", True),  # 'l' repeats
    ("ladle", True),  # 'l' repeats
    ("apple", True),  # 'p' repeats
    ("crumb", False),
    ("brown", False),
    ("mango", False),
    ("spicy", False),
])
def test_has_repeating_letters(word, expected):
    assert has_repeating_letters(word) is expected
    assert has_repeating_letters("spicy") is False