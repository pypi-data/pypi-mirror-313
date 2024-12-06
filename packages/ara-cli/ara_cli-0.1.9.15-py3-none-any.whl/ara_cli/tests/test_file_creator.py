from mock import Mock, patch, mock_open
from pathlib import Path
from ara_cli.artefact_creator import ArtefactCreator
import pytest


@patch("ara_cli.artefact_creator.os.path.exists")
def test_create_file_with_template_and_classifier(mock_exists):
    mock_exists.return_value = True

    # Mock open function to avoid file IO
    m = mock_open()
    with patch("builtins.open", m):
        fc = ArtefactCreator()
        fc.create_file("dummy_path", "template_path", "vision", "dummy_file")

    m.assert_any_call("template_path/template.vision", "r")
    m.assert_any_call("dummy_path", "w")


@patch("ara_cli.artefact_creator.os.path.exists")
def test_create_file_without_template_or_classifier(mock_exists):
    mock_exists.return_value = False

    # Mock open function to avoid file IO
    m = mock_open()
    with patch("builtins.open", m):
        fc = ArtefactCreator()
        fc.create_file("dummy_path")

    m.assert_any_call("dummy_path", "w")


def test_create_directory_with_valid_path():
    # Mock makedirs to avoid directory creation
    mock_fs = Mock()
    fc = ArtefactCreator(mock_fs)
    fc.create_directory("valid_path")

    mock_fs.makedirs.assert_called_with("valid_path", exist_ok=True)


def test_template_exists_with_valid_path():
    mock_fs = Mock()
    mock_fs.path.join.return_value = "full_path"
    mock_fs.path.isfile.return_value = True

    fc = ArtefactCreator(mock_fs)
    result = fc.template_exists("template_path", "template_name")

    assert result


def test_run_with_invalid_classifier_prints_error_message(capfd):
    fc = ArtefactCreator()
    fc.run("filename", "invalid_classifier")

    captured = capfd.readouterr()
    assert "Invalid classifier provided. Please provide a valid classifier." in captured.out


@patch("ara_cli.artefact_creator.input", return_value="n")
@patch("ara_cli.artefact_creator.os.path.exists", return_value=True)
def test_run_with_existing_file_does_not_overwrite(mock_input, mock_exists, capfd):
    fc = ArtefactCreator()
    fc.run("filename", "vision")

    captured = capfd.readouterr()
    assert "No changes were made to the existing file and directory." in captured.out


def test_create_artefact_exploration_success():
    creator = ArtefactCreator()

    # Mock the Path's exists method to always return True
    with patch.object(Path, "exists", return_value=True):
        with patch("builtins.open", mock_open()), patch("shutil.copyfile"):
            creator.create_artefact_prompt_files("./dest", "./source", "sample")


def test_create_artefact_exploration_source_not_found():
    creator = ArtefactCreator()

    with patch("pathlib.Path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            creator.create_artefact_prompt_files("./dest", "./source", "sample")


def test_create_artefact_exploration_dest_not_found():
    creator = ArtefactCreator()

    with patch.object(Path, "exists", lambda self: "source" in str(self)):
        with pytest.raises(NotADirectoryError):
            creator.create_artefact_prompt_files("./dest", "./source", "sample")
