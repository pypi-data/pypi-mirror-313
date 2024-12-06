import pytest
from unittest.mock import patch
from ara_cli.artefact import Artefact

mock_artefact_titles = ['Document', 'Report']
mock_ordered_classifiers = ['Document', 'Report']
mock_sub_directories = {
    'Document': 'documents',
    'Report': 'reports'
}


@pytest.fixture
def mock_classifier():
    with patch('ara_cli.artefact.Classifier') as MockClassifier:
        MockClassifier.artefact_titles.return_value = mock_artefact_titles
        MockClassifier.ordered_classifiers.return_value = mock_ordered_classifiers
        MockClassifier.get_artefact_classifier.side_effect = lambda x: 'Type1' if x == 'Document' else 'Type2'
        MockClassifier.get_sub_directory.side_effect = lambda x: mock_sub_directories[x]
        yield MockClassifier


@pytest.mark.parametrize(
    "content, expected_parent",
    [
        ("Contributes to: Parent Artefact Document", Artefact('Type1', 'Parent_Artefact')),
        ("Contributes to Parent Report", Artefact('Type2', 'Parent')),
        ("No parent defined here", None),
        ("", None),
    ]
)
def test_parent_property(mock_classifier, content, expected_parent):
    artefact = Artefact(classifier='Document', name='Test Artefact', content=content)

    parent = artefact.parent

    if expected_parent is None:
        assert parent is None
    else:
        assert parent is not None
        assert parent.name == expected_parent.name
        assert parent.classifier == expected_parent.classifier


@pytest.mark.parametrize(
    "initial_parent, expected_parent",
    [
        (Artefact('Document', 'Existing Parent'), Artefact('Document', 'Existing Parent')),
    ]
)
def test_parent_property_initial_parent(mock_classifier, initial_parent, expected_parent):
    artefact = Artefact(classifier='Document', name='Test Artefact', content="Contributes to: New Parent Document")
    artefact._parent = initial_parent  # Directly set _parent to simulate pre-existing condition

    parent = artefact.parent

    assert parent is not None
    assert parent.name == expected_parent.name
    assert parent.classifier == expected_parent.classifier


@pytest.mark.parametrize(
    "classifier, name, expected_file_path",
    [
        ('Document', 'Test Artefact', 'documents/Test_Artefact.Document'),
        ('Report', 'Another Report', 'reports/Another_Report.Report'),
        ('Document', 'Report with spaces', 'documents/Report_with_spaces.Document'),
    ]
)
def test_file_path_property(mock_classifier, classifier, name, expected_file_path):
    artefact = Artefact(classifier=classifier, name=name)
    file_path = artefact.file_path
    assert file_path == expected_file_path


@pytest.mark.parametrize(
    "content, expected_tags",
    [
        ("@tag1 @tag2 Some content here", {'tag1', 'tag2'}),
        ("@singleTag Content follows", {'singleTag'}),
        ("No tags in this content", set()),
        ("", set()),
        (None, set()),
        ("@mixedCase @AnotherTag @123numeric", {'mixedCase', 'AnotherTag', '123numeric'}),
        ("  @leadingSpaceTag  @another  ", {'leadingSpaceTag', 'another'}),
        ("Not a tag @notatag", set()),
    ]
)
def test_tags_property(mock_classifier, content, expected_tags):
    artefact = Artefact(classifier='Document', name='Test Artefact', content=content)
    tags = artefact.tags
    assert tags == expected_tags


@pytest.mark.parametrize(
    "initial_tags, content, expected_tags",
    [
        ({'preExistingTag'}, "@tag1 @tag2", {'preExistingTag'}),
        (None, "@tag1 @tag2", {'tag1', 'tag2'}),
        ({'anotherTag'}, "", {'anotherTag'}),
        (set(), "No tags in this content", set()),
    ]
)
def test_tags_property_when_tags_pre_set(mock_classifier, initial_tags, content, expected_tags):
    artefact = Artefact(classifier='Document', name='Test Artefact', content=content)
    artefact._tags = initial_tags  # Directly set _tags to simulate pre-existing condition

    tags = artefact.tags

    assert tags == expected_tags


@pytest.mark.parametrize(
    "content, expected_classifier, expected_name",
    [
        ("Document: Parent Artefact", 'Type1', 'Parent Artefact'),
        ("Report: Another Report", 'Type2', 'Another Report')
    ]
)
def test_from_content_valid(mock_classifier, content, expected_classifier, expected_name):
    artefact = Artefact.from_content(content)
    assert artefact.classifier == expected_classifier
    assert artefact.name == expected_name
    assert artefact.content == content


@pytest.mark.parametrize(
    "content",
    [
        "Invalid content without proper structure",
        "Classifier: Name: Missing title",
        "",
        None,
    ]
)
def test_from_content_invalid(mock_classifier, content):
    with pytest.raises(ValueError, match="Content does not contain valid artefact information"):
        Artefact.from_content(content)
