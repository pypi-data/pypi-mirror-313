from ara_cli.file_classifier import FileClassifier
from ara_cli.template_manager import DirectoryNavigator
from ara_cli.artefact_reader import ArtefactReader
from ara_cli.file_lister import list_files_in_directory
from ara_cli.artefact import Artefact
from ara_cli.list_filter import ListFilterMonad, ListFilter
import os


class ArtefactLister:
    def __init__(self, file_system=None):
        self.file_system = file_system or os

    def filter_list(self, classified_list, list_filter: ListFilter = None):
        if list_filter is None:
            return classified_list
        include_extension = list_filter.include_extension
        exclude_extension = list_filter.exclude_extension
        include_content = list_filter.include_content
        exclude_content = list_filter.exclude_content

        def artefact_content_retrieval(artefact):
            return artefact.content

        def artefact_path_retrieval(artefact):
            return artefact.file_path

        filter_monad = ListFilterMonad(classified_list, artefact_content_retrieval, artefact_path_retrieval)

        filter_monad.filter_by_extension(
            include=include_extension,
            exclude=exclude_extension
        )

        if include_content or exclude_content:
            filter_monad.filter_by_content(
                include=include_content,
                exclude=exclude_content
            )

        return filter_monad.get_files()

    def list_files(
        self,
        tags=None,
        navigate_to_target=False,
        list_filter: ListFilter | None = None
    ):
        # make sure this function is always called from the ara top level directory
        navigator = DirectoryNavigator()
        if navigate_to_target:
            navigator.navigate_to_target()

        file_classifier = FileClassifier(self.file_system)
        classified_files = file_classifier.classify_files(tags=tags)

        classified_files = self.filter_list(classified_files, list_filter)

        file_classifier.print_classified_files(classified_files)

    def list_branch(
        self,
        classifier,
        artefact_name,
        list_filter: ListFilter | None = None
    ):
        file_classifier = FileClassifier(os)
        artefacts_by_classifier = {classifier: []}
        ArtefactReader.step_through_value_chain(
            artefact_name=artefact_name,
            classifier=classifier,
            artefacts_by_classifier=artefacts_by_classifier
        )
        artefacts_by_classifier = self.filter_list(artefacts_by_classifier, list_filter)
        file_classifier.print_classified_files(artefacts_by_classifier)

    def list_children(
        self,
        classifier,
        artefact_name,
        list_filter: ListFilter | None = None
    ):
        file_classifier = FileClassifier(os)
        child_artefacts = ArtefactReader.find_children(
                artefact_name=artefact_name,
                classifier=classifier
        )
        child_artefacts = self.filter_list(child_artefacts, list_filter)
        file_classifier.print_classified_files(
            files_by_classifier=child_artefacts
        )

    def list_data(
        self,
        classifier,
        artefact_name,
        list_filter: ListFilter | None = None
    ):
        file_classifier = FileClassifier(os)
        classified_artefacts = file_classifier.classify_files()
        content, file_path = ArtefactReader.read_artefact(
            classifier=classifier,
            artefact_name=artefact_name
        )

        artefact = Artefact.from_content(content)
        file_path = next((classified_artefact.file_path for classified_artefact in classified_artefacts.get(classifier, []) if classified_artefact.name == artefact.name), artefact)

        file_path = os.path.splitext(file_path)[0] + '.data'
        list_files_in_directory(file_path, list_filter)
