from ara_cli.ara_config import ensure_directory_exists
from unittest.mock import patch, call


def test_ensure_directory_exists_when_directory_does_not_exist():
    directory = "/some/non/existent/directory"

    with patch("ara_cli.ara_config.exists", return_value=False) as mock_exists:
        with patch("ara_cli.ara_config.os.makedirs") as mock_makedirs:
            result = ensure_directory_exists(directory)

            mock_exists.assert_called_once_with(directory)
            mock_makedirs.assert_called_once_with(directory)
            assert result == directory


def test_ensure_directory_exists_when_directory_exists():
    directory = "/some/existent/directory"

    with patch("ara_cli.ara_config.exists", return_value=True) as mock_exists:
        with patch("ara_cli.ara_config.os.makedirs") as mock_makedirs:
            result = ensure_directory_exists(directory)

            mock_exists.assert_called_once_with(directory)
            mock_makedirs.assert_not_called()
            assert result == directory
