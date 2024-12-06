import pytest
from unittest.mock import patch, mock_open, Mock
from ara_cli.artefact_reader import ArtefactReader
from ara_cli.artefact import Artefact


@pytest.mark.parametrize("artefact_name, classifier, is_valid, file_exists, expected_output", [
    ("artefact1", "valid_classifier", True, True, ("file content", "/valid_classifier/artefact1.valid_classifier")),
    ("artefact2", "invalid_classifier", False, True, None),
    ("artefact3", "valid_classifier", True, False, None),
])
def test_read_artefact(artefact_name, classifier, is_valid, file_exists, expected_output):
    original_directory = "/original/directory"

    with patch('os.getcwd', return_value=original_directory), \
         patch('os.chdir') as mock_chdir, \
         patch('ara_cli.directory_navigator.DirectoryNavigator.navigate_to_target'), \
         patch('ara_cli.classifier.Classifier.is_valid_classifier', return_value=is_valid), \
         patch('ara_cli.classifier.Classifier.get_sub_directory', return_value=f"/{classifier}"), \
         patch('os.path.exists', return_value=file_exists), \
         patch('builtins.open', mock_open(read_data="file content")) as mock_file:

        if expected_output is None:
            expected_content, expected_file_path = None, None
        else:
            expected_content, expected_file_path = expected_output

        content, file_path = ArtefactReader.read_artefact(artefact_name, classifier)

        # Check if the content and file path match expected output
        assert content == expected_content
        assert file_path == expected_file_path

        # Check the directory was changed back to original
        mock_chdir.assert_called_with(original_directory)

        if not is_valid:
            mock_file.assert_not_called()
        elif not file_exists:
            mock_file.assert_not_called()
        else:
            mock_file.assert_called_once_with(expected_file_path, 'r')


@pytest.mark.parametrize("artefact_content, artefact_titles, expected_output", [
    ("Contributes to: parent_name SomeTitle", ["SomeTitle"], ("parent_name", "SomeTitle")),
    ("Contributes to parent_name SomeTitle", ["SomeTitle"], ("parent_name", "SomeTitle")),
    ("Contributes to : parent_name AnotherTitle", ["SomeTitle", "AnotherTitle"], ("parent_name", "AnotherTitle")),
    ("No contribution information here.", ["SomeTitle"], (None, None)),
    ("Contributes to : parent_name NotListedTitle", ["SomeTitle"], (None, None)),
])
def test_extract_parent_tree(artefact_content, artefact_titles, expected_output):
    with patch('ara_cli.classifier.Classifier.artefact_titles', return_value=artefact_titles):
        parent_name, parent_type = ArtefactReader.extract_parent_tree(artefact_content)
        assert (parent_name, parent_type) == expected_output


@pytest.mark.parametrize("artefact_name, classifier, artefact_content, artefact_parent, expected_calls", [
    ("artefact1", "classifier1", "content1", None, [("artefact1", "classifier1")]),
    ("artefact2", "classifier2", "content2", Mock(name="parent_artefact", classifier="parent_classifier"), 
     [("artefact2", "classifier2"), ("parent_artefact", "parent_classifier")]),
    ("artefact3", "classifier3", "content3", None, [("artefact3", "classifier3")]),
])
def test_step_through_value_chain(artefact_name, classifier, artefact_content, artefact_parent, expected_calls):
    artefact_mock = Mock(spec=Artefact)
    artefact_mock.name = artefact_name
    artefact_mock.parent = artefact_parent
    
    artefact_by_classifier = {}

    with patch('ara_cli.artefact_reader.ArtefactReader.read_artefact', return_value=(artefact_content, "file_path")), \
         patch('ara_cli.artefact.Artefact.from_content', return_value=artefact_mock) as mock_from_content:
        
        ArtefactReader.step_through_value_chain(artefact_name, classifier, artefact_by_classifier)

        # Check if artefact was added to the artefacts_by_classifier
        assert artefact_mock in artefact_by_classifier[classifier]

        # Check if the recursive calls are made correctly
        for call in expected_calls:
            artefact_name_call, classifier_call = call
            mock_from_content.assert_any_call(artefact_content)
            artefact_mock.parent = artefact_parent

        # Ensure no duplicate artefacts are added
        ArtefactReader.step_through_value_chain(artefact_name, classifier, artefact_by_classifier)
        assert len(artefact_by_classifier[classifier]) == 1
