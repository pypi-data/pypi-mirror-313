import pytest
from unittest.mock import patch, mock_open
from ara_cli.list_filter import ListFilterMonad, ListFilter, filter_list


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


@pytest.mark.parametrize("input_files, expected_files", [
    ({"group1": ["file1.txt"]}, {"group1": ["file1.txt"]}),  # Case when input is a dict
    (["file1.txt", "file2.log"], {"default": ["file1.txt", "file2.log"]})  # Case when input is not a dict
])
def test_list_filter_monad_initialization(input_files, expected_files):
    monad = ListFilterMonad(input_files)
    assert monad.files == expected_files


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


def test_default_content_retrieval():
    mock_data = "Mock file data"
    with patch("builtins.open", mock_open(read_data=mock_data)) as mocked_file:
        content = ListFilterMonad.default_content_retrieval("dummy_path")
        assert content == mock_data
        mocked_file.assert_called_once_with("dummy_path", 'r')


def test_default_content_retrieval_exception():
    with patch("builtins.open", side_effect=Exception("Mocked exception")) as mocked_file:
        content = ListFilterMonad.default_content_retrieval("dummy_path")
        assert content == ""  # Expect empty string on exception
        mocked_file.assert_called_once_with("dummy_path", 'r')


@pytest.mark.parametrize("include_content, exclude_content, expected", [
    (["Hello"], None, ["file1.txt"]),  # Only include files containing "Hello"
    (None, ["Error"], ["file1.txt", "file3.md"]),  # Exclude files containing "Error"
    (["Markdown"], ["Error"], ["file3.md"]),  # Include "Markdown" and exclude "Error"
    (["Hello", "Markdown"], None, ["file1.txt", "file3.md"]),  # Include either "Hello" or "Markdown"
    (None, None, ["file1.txt", "file2.log", "file3.md"])  # No filtering
])
def test_filter_by_content(sample_files, include_content, exclude_content, expected):
    with patch("ara_cli.list_filter.ListFilterMonad.default_content_retrieval", side_effect=mock_content_retrieval):
        monad = ListFilterMonad(sample_files)
        filtered_files = monad.filter_by_content(include=include_content, exclude=exclude_content).get_files()
        assert filtered_files == expected


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


@pytest.mark.parametrize("list_filter, expected", [
    (None, {"default":["file1.txt", "file2.log", "file3.md"]}),  # No filtering
    (ListFilter(include_extension=[".txt"], exclude_extension=None, include_content=None, exclude_content=None), ["file1.txt"]),  # Include only .txt
    (ListFilter(include_extension=None, exclude_extension=[".log"], include_content=None, exclude_content=None), ["file1.txt", "file3.md"]),  # Exclude .log
    (ListFilter(include_extension=None, exclude_extension=None, include_content=["Hello"], exclude_content=None), ["file1.txt"]),  # Include content "Hello"
    (ListFilter(include_extension=None, exclude_extension=None, include_content=None, exclude_content=["Error"]), ["file1.txt", "file3.md"]),  # Exclude content "Error"
    (ListFilter(include_extension=[".md"], exclude_extension=None, include_content=["Markdown"], exclude_content=["Error"]), ["file3.md"]),  # Complex filter
])
def test_filter_list(sample_files, list_filter, expected):
    with patch("ara_cli.list_filter.ListFilterMonad.default_content_retrieval", side_effect=mock_content_retrieval):
        result = filter_list(
            list_to_filter=sample_files,
            list_filter=list_filter
        )
        assert result == expected
