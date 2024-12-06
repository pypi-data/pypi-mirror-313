from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal, Optional
from ara_cli.classifier import Classifier
import re
import os


@dataclass
class Artefact:
    classifier: Literal(Classifier.ordered_classifiers())
    name: str
    content: str | None = None
    _parent: Artefact | None = field(init=False, default=None)
    _file_path: Optional[str] = None
    _tags: set[str] | None = None

    @property
    def parent(self) -> Artefact | None:
        if self._parent is not None:
            return self._parent

        if self.content is None:
            with open(self.file_path, 'r') as file:
                self.content = file.read()

        artefact_titles = Classifier.artefact_titles()
        title_segment = '|'.join(artefact_titles)

        regex_pattern = rf'Contributes to\s*:*\s*(.*)\s+({title_segment}).*'
        regex = re.compile(regex_pattern)
        match = re.search(regex, self.content)

        if match:
            parent_name = match.group(1).strip()
            parent_name = parent_name.replace(' ', '_')
            parent_title = match.group(2).strip()
            parent_type = Classifier.get_artefact_classifier(parent_title)
            self._parent = Artefact(classifier=parent_type, name=parent_name)

        return self._parent

    @property
    def file_path(self) -> str:
        if self._file_path is None:
            sub_directory = Classifier.get_sub_directory(self.classifier)
            underscore_name = self.name.replace(' ', '_')
            self._file_path = f"{sub_directory}/{underscore_name}.{self.classifier}"
        return self._file_path

    @property
    def tags(self) -> set[str]:
        if self._tags is not None:
            return self._tags

        if self.content is None:
            return set()

        lines = self.content.splitlines()
        first_line = lines[0].strip() if lines else ""

        if first_line.startswith('@'):
            self._tags = {tag[1:] for tag in first_line.split() if tag.startswith('@')}
        else:
            self._tags = set()

        return self._tags

    @classmethod
    def from_content(cls, content: str) -> Artefact:
        """
        Create an Artefact object from the given content.
        """
        error_message = "Content does not contain valid artefact information"

        if content is None:
            raise ValueError(error_message)

        artefact_titles = Classifier.artefact_titles()
        title_segment = '|'.join(artefact_titles)

        regex_pattern = rf'({title_segment})\s*:*\s*(.*)\s*'
        regex = re.compile(regex_pattern)
        match = re.search(regex, content)

        if not match:
            raise ValueError(error_message)

        title = match.group(1).strip()
        classifier = Classifier.get_artefact_classifier(title)
        name = match.group(2).strip()

        return cls(classifier=classifier, name=name, content=content)
