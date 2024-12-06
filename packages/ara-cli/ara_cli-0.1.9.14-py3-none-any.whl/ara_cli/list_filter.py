from dataclasses import dataclass


@dataclass
class ListFilter:
    include_extension: list[str] | None = None
    exclude_extension: list[str] | None = None
    include_content: list[str] | None = None
    exclude_content: list[str] | None = None


class ListFilterMonad:
    def __init__(self, files, content_retrieval_strategy=None, file_path_retrieval=None):
        if isinstance(files, dict):
            self.files = files
        else:
            self.files = {"default": files}
        self.content_retrieval_strategy = content_retrieval_strategy or self.default_content_retrieval
        self.file_path_retrieval = file_path_retrieval or self.default_file_path_retrieval

    def bind(self, func):
        self.files = func(self.files)
        return self

    @staticmethod
    def default_content_retrieval(file):
        # Default strategy assumes file is a path and attempts to read it
        try:
            with open(file, 'r') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {file}: {e}")
            return ""

    @staticmethod
    def default_file_path_retrieval(file):
        return file

    def _get_extension(self, file):
        if isinstance(file, Artefact):
            return file.file_path
        return file

    def filter_by_extension(self, include=None, exclude=None):
        def filter_logic(files):
            for key, original_files in files.items():
                filtered_files = original_files
                if include:
                    filtered_files = [f for f in filtered_files if any(self.file_path_retrieval(f).endswith(ext) for ext in include)]
                if exclude:
                    filtered_files = [f for f in filtered_files if not any(self.file_path_retrieval(f).endswith(ext) for ext in exclude)]
                files[key] = filtered_files
            return files
        return self.bind(filter_logic)

    # def filter_by_content(self, include=None, exclude=None):
    #     def filter_logic(files):
    #         for key, files in files.items():
    #             filtered_files = []
    #             for file in files:
    #                 content = self.content_retrieval_strategy(file)
    #                 include_match = include and any(inc in content for inc in include)
    #                 exclude_match = exclude and any(exc in content for exc in exclude)
    #                 if include_match and not exclude_match:
    #                     filtered_files.append(file)
    #             files[key] = filtered_files
    #         return files
    #     return self.bind(filter_logic)

    def get_files(self):
        # Return the files dictionary. If it only contains the "default" key, return its list.
        if len(self.files) == 1 and "default" in self.files:
            return self.files["default"]
        return self.files
