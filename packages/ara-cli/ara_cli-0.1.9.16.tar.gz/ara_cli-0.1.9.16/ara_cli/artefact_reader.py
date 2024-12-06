from ara_cli.directory_navigator import DirectoryNavigator
from ara_cli.classifier import Classifier
from ara_cli.file_classifier import FileClassifier
from ara_cli.artefact import Artefact
import os
import re


class ArtefactReader:
    @staticmethod
    def read_artefact(artefact_name, classifier):
        original_directory = os.getcwd()
        navigator = DirectoryNavigator()
        navigator.navigate_to_target()

        if not Classifier.is_valid_classifier(classifier):
            print("Invalid classifier provided. Please provide a valid classifier.")
            os.chdir(original_directory)
            return None, None

        sub_directory = Classifier.get_sub_directory(classifier)
        file_path = os.path.join(sub_directory, f"{artefact_name}.{classifier}")

        file_exists = os.path.exists(file_path)

        if not file_exists:
            print(f"File \"{file_path}\" not found")
            os.chdir(original_directory)
            return None, None

        with open(file_path, 'r') as file:
            content = file.read()

        os.chdir(original_directory)

        return content, file_path

    @staticmethod
    def extract_parent_tree(artefact_content):
        artefact_titles = Classifier.artefact_titles()
        title_segment = '|'.join(artefact_titles)

        regex_pattern = rf'Contributes to\s*:*\s*(.*)\s+({title_segment}).*'
        regex = re.compile(regex_pattern)
        match = re.search(regex, artefact_content)
        if not match:
            return None, None

        parent_name = match.group(1).strip()
        parent_type = match.group(2).strip()

        return parent_name, parent_type

    @staticmethod
    def find_children(artefact_name, classifier, artefacts_by_classifier={}, classified_artefacts=None):

        def merge_dicts(dict1, dict2):
            from collections import defaultdict

            merged_dict = defaultdict(list)

            # Add items from the first dictionary
            for key, artefact_list in dict1.items():
                merged_dict[key].extend(artefact_list)

            # Add items from the second dictionary
            for key, artefact_list in dict2.items():
                merged_dict[key].extend(artefact_list)

            return dict(merged_dict)

        if classified_artefacts is None:
            file_classifier = FileClassifier(os)
            classified_artefacts = file_classifier.classify_files()

        filtered_artefacts = {}
        for key, artefact_list in classified_artefacts.items():
            filtered_list = [
                artefact for artefact in artefact_list
                if artefact.parent and
                artefact.parent.name == artefact_name and
                artefact.parent.classifier == classifier
            ]
            if filtered_list:
                filtered_artefacts[key] = filtered_list

        merged_dict = merge_dicts(artefacts_by_classifier, filtered_artefacts)

        return merged_dict

    @staticmethod
    def step_through_value_chain(
            artefact_name,
            classifier,
            artefacts_by_classifier={},
            classified_artefacts: dict[str, list[Artefact]] | None = None
            ):
        if classified_artefacts is None:
            file_classifier = FileClassifier(os)
            classified_artefacts = file_classifier.classify_files()

        content, file_path = ArtefactReader.read_artefact(artefact_name, classifier)

        artefact = Artefact.from_content(content)
        artefact_path = next((classified_artefact.file_path for classified_artefact in classified_artefacts.get(classifier, []) if classified_artefact.name == artefact.name), artefact)
        artefact._file_path = artefact_path

        if classifier not in artefacts_by_classifier:
            artefacts_by_classifier[classifier] = []

        matching_artefacts = list(filter(lambda x: x.name == artefact.name, artefacts_by_classifier[classifier]))
        if len(matching_artefacts) != 0:
            return

        artefacts_by_classifier[classifier].append(artefact)
        parent = artefact.parent
        if parent:
            parent_name = parent.name
            parent_classifier = parent.classifier
            ArtefactReader.step_through_value_chain(
                artefact_name=parent_name,
                classifier=parent_classifier,
                artefacts_by_classifier=artefacts_by_classifier,
                classified_artefacts=classified_artefacts
            )
