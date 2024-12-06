import pytest
from unittest.mock import Mock, patch
from ara_cli.tag_extractor import TagExtractor


@pytest.fixture
def mock_file_system():
    return Mock()


@pytest.fixture
def mock_navigator():
    return Mock()


@pytest.fixture
def mock_file_classifier():
    return Mock()


def test_extract_tags_no_navigation(mock_file_system, mock_navigator, mock_file_classifier):
    mock_file_classifier.classify_files.return_value = {
        'type1': [Mock(tags={'tag1', 'tag2'}), Mock(tags={'tag2', 'tag3'})],
        'type2': [Mock(tags={'tag3', 'tag4'})],
    }
    with patch('ara_cli.template_manager.DirectoryNavigator', return_value=mock_navigator), \
         patch('ara_cli.file_classifier.FileClassifier', return_value=mock_file_classifier):

        tag_extractor = TagExtractor(file_system=mock_file_system)

        tags = tag_extractor.extract_tags(navigate_to_target=False)

        assert tags == ['tag1', 'tag2', 'tag3', 'tag4']
        mock_navigator.navigate_to_target.assert_not_called()


def test_extract_tags_with_navigation(mock_file_system, mock_navigator, mock_file_classifier):

    mock_file_classifier.classify_files.return_value = {
        'type1': [Mock(tags={'tag1', 'tag2'}), Mock(tags={'tag2', 'tag3'})]
    }
    with patch('ara_cli.template_manager.DirectoryNavigator', return_value=mock_navigator), \
         patch('ara_cli.file_classifier.FileClassifier', return_value=mock_file_classifier):

        tag_extractor = TagExtractor(file_system=mock_file_system)

        tags = tag_extractor.extract_tags(navigate_to_target=True)

        assert tags == ['tag1', 'tag2', 'tag3']
        mock_navigator.navigate_to_target.assert_called_once()
