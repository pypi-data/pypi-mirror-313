from mock import patch
from unittest.mock import call, mock_open
from ara_cli.artefact_renamer import ArtefactRenamer
from ara_cli.classifier import Classifier
import mock
import pytest
import os
import shutil


@pytest.fixture(autouse=True)
def cleanup():
    """
    A fixture to clean up the 'new_name.data' directory after each test case.
    """
    yield  # This is where the test runs
    new_data_dir = "ara/userstories/new_name.data"
    if os.path.exists(new_data_dir):
        shutil.rmtree(new_data_dir)


@patch("ara_cli.artefact_renamer.os.path.exists")
def test_rename_checks_filename_exists(mock_exists):
    mock_exists.return_value = False
    ar = ArtefactRenamer(os)
    with pytest.raises(FileNotFoundError):
        ar.rename("nonexistent_file", "new_file", "vision")

def test_rename_checks_classifier_valid():
    ar = ArtefactRenamer(os)
    with pytest.raises(ValueError):
        ar.rename("existing_file", "new_file", "invalid_classifier")


def test_rename_checks_new_name_provided():
    ar = ArtefactRenamer(os)
    with pytest.raises(ValueError):
        ar.rename("existing_file", None, None)


@patch("builtins.open", new_callable=mock_open, read_data="Vision: Old Title\nOther content.")
@patch("ara_cli.artefact_renamer.os.rename")
@patch("ara_cli.artefact_renamer.os.path.exists", side_effect=[True, True, False, False, True])
def test_rename_filename_with_new_name(mock_exists, mock_rename, mock_open):
    ar = ArtefactRenamer(os)
    ar.rename("existing_file", "new_file", "vision")
    assert mock_rename.call_count == 2
    mock_rename.assert_has_calls([
        call("vision/existing_file.vision", "vision/new_file.vision"),
        call("vision/existing_file.data", "vision/new_file.data")
    ])


@patch("ara_cli.artefact_renamer.os.path.exists", side_effect=[True, True, True, False])
def test_rename_throws_error_if_new_file_or_directory_exists(mock_exists):
    ar = ArtefactRenamer(os)
    with pytest.raises(FileExistsError):
        ar.rename("existing_file", "existing_file", "vision")


@patch("ara_cli.artefact_renamer.os.path.exists", side_effect=[True, False, False])
def test_rename_checks_related_data_folder_exists(mock_exists):
    ar = ArtefactRenamer(os)
    with pytest.raises(FileNotFoundError):
        ar.rename("old_name", "new_name", "userstory")


@patch("builtins.open", new_callable=mock_open, read_data="Userstory: Old Title\nOther content.")
@patch("ara_cli.artefact_renamer.os.rename")
@patch("ara_cli.artefact_renamer.os.path.exists", side_effect=[True, True, False, False, True])
def test_rename_also_renames_related_data_folder(mock_exists, mock_rename, mock_open):
    ar = ArtefactRenamer(os)
    ar.rename("old_name", "new_name", "userstory")
    assert mock_rename.call_count == 2
    mock_rename.assert_has_calls([
        call("userstories/old_name.userstory", "userstories/new_name.userstory"),
        call("userstories/old_name.data", "userstories/new_name.data")
    ])


@patch("ara_cli.artefact_renamer.os.path.exists", side_effect=[True, True, True])
def test_rename_throws_error_if_new_file_path_exists(mock_exists):
    ar = ArtefactRenamer()
    with pytest.raises(FileExistsError):
        ar.rename("old_name", "new_name", "userstory")


@patch("ara_cli.artefact_renamer.os.path.exists", side_effect=[True, True, False, True])
def test_rename_throws_error_if_new_data_directory_exists(mock_exists):
    ar = ArtefactRenamer()
    with pytest.raises(FileExistsError):
        ar.rename("old_name", "new_name", "userstory")


@pytest.mark.parametrize("classifier,artefact_name,read_data_prefix,old_title,new_title", [
    ("vision", "Vision", "Vision: ", "Old Title", "New title"),
    ("businessgoal", "Businessgoal", "Businessgoal: ", "Old Title", "New title"),
    ("capability", "Capability", "Capability: ", "Old Title", "New title"),
    ("keyfeature", "Keyfeature", "Keyfeature: ", "Old Title", "New title"),
    ("feature", "Feature", "Feature: ", "Old Title", "New title"),
    ("epic", "Epic", "Epic: ", "Old Title", "New title"),
    ("userstory", "Userstory", "Userstory: ", "Old Title", "New title"),
    ("task", "Task", "Task: ", "Old Title", "New title"),
    ("task", "Task list", "Task list: ", "Old Title", "New title"),
    ("example", "Example", "Example: ", "Old Title", "New title"),
])
@patch("builtins.open", new_callable=mock_open)
def test_update_title_in_artefact(mock_file, classifier, artefact_name, read_data_prefix, old_title, new_title):
    ar = ArtefactRenamer(os)
    read_data = f"{read_data_prefix}{old_title}\nOther content that remains unchanged."
    mock_file.return_value.read = mock.Mock(return_value=read_data)
    artefact_path = f"path/to/{classifier}.artefact"

    # Ensure that the mock for get_artefact_title returns the prefix without an extra colon and space
    with patch.object(Classifier, 'get_artefact_title', return_value=artefact_name):
        ar._update_title_in_artefact(artefact_path, new_title, classifier)

    # Check that the file was opened for reading
    mock_file.assert_any_call(artefact_path, 'r')
    # Check that the file was opened for writing
    mock_file.assert_any_call(artefact_path, 'w')
    # Check that the file write was called with the correct new content
    expected_content = read_data.replace(f"{read_data_prefix}{old_title}", f"{read_data_prefix}{new_title}")
    mock_file().write.assert_called_with(expected_content)


@patch("builtins.open", new_callable=mock_open)
def test_update_title_invalid_classifier(mocker):
    ar = ArtefactRenamer()
    with pytest.raises(ValueError):
        ar._update_title_in_artefact("path", "title", "invalid_classifier")


@patch("builtins.open", new_callable=mock_open)
@patch("ara_cli.artefact_renamer.Classifier.get_artefact_title", return_value="Vision")
def test_update_title_no_title_line(mock_get_artefact_title, mock_file):
    ar = ArtefactRenamer()

    read_data = "content that remains unchanged."
    mock_file.return_value.read = mock.Mock(return_value=read_data)
    artefact_path = "path/to/artefact.vision"

    with pytest.raises(ValueError):
        ar._update_title_in_artefact(artefact_path, "title", "vision")
