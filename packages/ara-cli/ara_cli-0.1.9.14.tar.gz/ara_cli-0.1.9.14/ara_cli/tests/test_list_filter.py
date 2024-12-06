import pytest
from unittest.mock import patch, mock_open
from ara_cli.list_filter import ListFilterMonad


@pytest.fixture
def sample_files():
    return {
        "default": ["file1.txt", "file2.log", "file3.md"]
    }


def mock_content_retrieval(file):
    contents = {
        "file1.txt": "Hello World",
        "file2.log": "Error log",
        "file3.md": "Markdown content"
    }
    return contents.get(file, "")


@pytest.mark.parametrize("include_ext, exclude_ext, expected", [
    ([".txt", ".md"], None, ["file1.txt", "file3.md"]),
    (None, [".log"], ["file1.txt", "file3.md"]),
    ([".log"], [".txt"], ["file2.log"]),
    (None, None, ["file1.txt", "file2.log", "file3.md"])
])
def test_filter_by_extension(sample_files, include_ext, exclude_ext, expected):
    monad = ListFilterMonad(sample_files)
    filtered_files = monad.filter_by_extension(include=include_ext, exclude=exclude_ext).get_files()
    assert filtered_files == expected


# @pytest.mark.parametrize("include_content, exclude_content, expected", [
#     (["Hello"], None, ["file1.txt"]),
#     (None, ["Error"], ["file1.txt", "file3.md"]),
#     (["Error"], ["Hello"], ["file2.log"]),
#     (["Hello", "Markdown"], None, ["file1.txt", "file3.md"]),
#     (None, None, ["file1.txt", "file2.log", "file3.md"])
# ])
# def test_filter_by_content(sample_files, include_content, exclude_content, expected):
#     monad = ListFilterMonad(sample_files, content_retrieval_strategy=mock_content_retrieval)
#     filtered_files = monad.filter_by_content(include=include_content, exclude=exclude_content).get_files()
#     assert filtered_files == expected


def test_default_content_retrieval():
    mock_data = "Mock file data"
    with patch("builtins.open", mock_open(read_data=mock_data)) as mocked_file:
        content = ListFilterMonad.default_content_retrieval("dummy_path")
        assert content == mock_data
        mocked_file.assert_called_once_with("dummy_path", 'r')


def test_get_files_default_key(sample_files):
    monad = ListFilterMonad(sample_files)
    assert monad.get_files() == ["file1.txt", "file2.log", "file3.md"]


def test_get_files_multiple_keys():
    files = {
        "group1": ["file1.txt"],
        "group2": ["file2.log"]
    }
    monad = ListFilterMonad(files)
    assert monad.get_files() == files
