import os


class TagExtractor:
    def __init__(self, file_system=None):
        self.file_system = file_system or os

    def extract_tags(self, navigate_to_target=False):
        from ara_cli.template_manager import DirectoryNavigator
        from ara_cli.file_classifier import FileClassifier

        navigator = DirectoryNavigator()
        if navigate_to_target:
            navigator.navigate_to_target()

        file_classifier = FileClassifier(self.file_system)
        classified_files = file_classifier.classify_files(read_content=True)

        unique_tags = set()

        for artefacts in classified_files.values():
            for artefact in artefacts:
                unique_tags.update(artefact.tags)

        sorted_tags = sorted(unique_tags)
        return sorted_tags
