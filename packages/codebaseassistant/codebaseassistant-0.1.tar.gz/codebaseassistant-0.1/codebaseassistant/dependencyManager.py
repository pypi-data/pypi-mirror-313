import os
from .fileCollectionProtocol import FileCollectionProtocol


class SupportedFileTypeData:
    def __init__(self, extension, has_dependencies=True):
        """
        Represents data for a supported file type.

        :param extension: The file extension (e.g., '.py', '.js').
        :param has_dependencies: Indicates if this file type is expected to have dependencies.
        """
        self.extension = extension
        self.has_dependencies = has_dependencies

    def __repr__(self):
        return f"SupportedFileTypeData(extension='{self.extension}', has_dependencies={self.has_dependencies})"


class DependencyManager:
    def __init__(self, root_folder: str, file_collection_protocol: FileCollectionProtocol = FileCollectionProtocol()):
        """
        Initializes the DependencyManager and builds the file map.

        :param root_folder: The root folder of the project.
        """
        self.root_folder = root_folder
        self.file_collection_protocol = file_collection_protocol
        self.supported_file_types = [
            SupportedFileTypeData(".py"),
            SupportedFileTypeData(".js"),
            SupportedFileTypeData(".cs"),
            SupportedFileTypeData(".cpp"),
            SupportedFileTypeData(".h"),
            SupportedFileTypeData(".bat", has_dependencies=False),
            SupportedFileTypeData(".vbs", has_dependencies=False),
            SupportedFileTypeData(".txt", has_dependencies=False),
            SupportedFileTypeData(".cvs", has_dependencies=False),
            SupportedFileTypeData(".json", has_dependencies=False),
        ]

        self.dependency_processor: DependencyProcessorBase = DependencyProcessorDefault()
        self.file_map = self._build_file_map()

    def _build_file_map(self):
        """
        Builds a nested dictionary representing the folder structure and files
        using the file_collection_protocol's list of files and folders.

        :return: A nested dictionary representing the file map.
        """
        file_map = {}

        for file_or_folder in self.file_collection_protocol.files:
            parts = os.path.relpath(
                file_or_folder, self.root_folder).split(os.sep)
            current_level = file_map

            for part in parts[:-1]:  # Navigate to the correct folder level
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]

            # Handle the file or folder
            if os.path.isfile(file_or_folder):
                file_name, file_ext = os.path.splitext(parts[-1])
                current_level[file_name] = {
                    "name": parts[-1],
                    "path": file_or_folder,
                    "extension": file_ext,
                    "dependencies": []
                }
            else:  # Add empty dict for folders
                if parts[-1] not in current_level:
                    current_level[parts[-1]] = {}

        return file_map

    def populate_dependencies(self):
        """
        Iterates over the entire file map and populates dependencies for supported files.
        """
        def recurse_and_populate(file_map):
            for key, value in file_map.items():
                if isinstance(value, dict):
                    # If this is a file node
                    if "path" in value and self._is_supported_language(value["extension"]):
                        supported_type = self._get_supported_type_data(
                            value["extension"])
                        if supported_type.has_dependencies:
                            value["dependencies"] = self._get_file_dependencies(
                                value["path"])
                    else:
                        # Recurse into subdirectories
                        recurse_and_populate(value)

        recurse_and_populate(self.file_map)

    def _is_supported_language(self, extension):
        """
        Checks if a file extension corresponds to a supported programming language.

        :param extension: The file extension (e.g., '.py', '.js').
        :return: True if supported, False otherwise.
        """
        return any(file_type.extension == extension for file_type in self.supported_file_types)

    def _get_supported_type_data(self, extension):
        """
        Retrieves the SupportedFileTypeData object for a given file extension.

        :param extension: The file extension (e.g., '.py', '.js').
        :return: A SupportedFileTypeData object or None if not found.
        """
        for file_type in self.supported_file_types:
            if file_type.extension == extension:
                return file_type
        return None

    def _get_file_dependencies(self, file_path):
        """
        Determines dependencies for a single file using the dependency processor.

        :param file_path: Path to the file.
        :return: A list of Dependency instances.
        """
        if self.dependency_processor:
            dependencies = self.dependency_processor.process_dependencies(
                file_path)
            if not isinstance(dependencies, list):
                print(
                    "Warning: Processed dependencies are not a list. Returning an empty list.")
                return []
            else:
                return dependencies
        return []

    def __repr__(self):
        return f"DependencyManager(root_folder='{self.root_folder}', file_map={self.file_map})"


class DependencyProcessorBase:
    def process_dependencies(self, file_path: str):
        """
        Process dependencies for a given file.

        :param file_path: Path to the file to analyze for dependencies.
        :return: A list of Dependency instances.
        """
        raise NotImplementedError(
            "This method should be implemented by subclasses.")


class DependencyProcessorDefault(DependencyProcessorBase):
    def __init__(self) -> None:
        super().__init__()

    def process_dependencies(self, file_path: str):
        pass
