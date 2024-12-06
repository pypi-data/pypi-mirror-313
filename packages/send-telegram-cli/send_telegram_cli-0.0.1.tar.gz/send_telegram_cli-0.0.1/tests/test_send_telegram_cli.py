from send_telegram_cli import app
import pytest
import subprocess
import json
from unittest.mock import patch, MagicMock
from send_telegram_cli.app import main as mainrun, get_key, user_dir


def test_create_parser():
    parser = app.create_parser()
    result = parser.parse_args(["-m", "hello"])
    assert result.message == ["hello"]
    assert result.attachment is None
    assert result.bot is None
    assert result.chatid is None


@pytest.fixture
def mock_keys():
    """Fixture to set up mock keys for testing."""
    keys = {
        "test_bot": "123456:ABC-DEF1234ghIkl-zyx57W2P0s",
        "test_chatid": "987654321",
    }
    keys_file = user_dir() / "dummy_bot_keys.json"
    keys_file.parent.mkdir(parents=True, exist_ok=True)
    keys_file.write_text(json.dumps(keys))
    yield
    keys_file.unlink()  # Clean up after test


@patch("subprocess.call")
@patch("send_telegram_cli.app.get_key")
@patch("send_telegram_cli.app.get_default")
def test_main_send_message(
    mock_get_default, mock_get_key, mock_subprocess_call, mock_keys
):
    """Test sending a message using the main function."""
    # Arrange
    mock_get_default.side_effect = (
        lambda name: "test_bot" if name == "bot" else "test_chatid"
    )
    mock_get_key.side_effect = (
        lambda key_type, name: "123456:ABC-DEF1234ghIkl-zyx57W2P0s"
        if name == "test_bot"
        else "987654321"
    )

    # Simulate command line arguments
    test_args = ["sendtele", "-m", "Hello, World!"]

    with patch("sys.argv", test_args):
        mainrun()

    # Assert
    mock_subprocess_call.assert_called_once()
    assert (
        mock_subprocess_call.call_args[0][0][0] == "curl"
    )  # Check if curl command is called
    assert (
        "Hello, World!" in mock_subprocess_call.call_args[0][0][-1]
    )  # Check if message is included
