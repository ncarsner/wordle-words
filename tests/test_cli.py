import pytest
from src.wordle_manager.cli import parse_args


@pytest.mark.parametrize(
    "sys_argv, expected_action",
    [
        (["wordle-manager", "stats"], "stats"),
        (["wordle-manager", "dedup"], "dedup"),
        (["wordle-manager", "sort"], "sort"),
        (["wordle-manager", "clean"], "clean"),
    ],
)
def test_parse_args_basic_actions(monkeypatch, sys_argv, expected_action):
    """Test parsing basic actions"""
    # Arrange
    monkeypatch.setattr("sys.argv", sys_argv)

    # Act
    args = parse_args()

    # Assert
    assert args.action == expected_action
    assert not hasattr(args, "num")
    assert not hasattr(args, "word")
