import os
from typing import List


class FileCollectionProtocol:
    """
    A base class for collecting files and folders from a directory based on custom checks.
    """

    def __init__(self, directory: str) -> None:
        """
        Initialize the FileCollectionProtocol.

        :param directory: The directory to process files from.
        """
        if not os.path.isdir(directory):
            raise ValueError(f"Invalid directory: {directory}")
        self.directory = directory
        self.files: List[str] = []

    def process(self):
        """
        Populates the `files` list with absolute paths of files and folders
        that pass the checks defined in the class.
        """
        self.files = [
            os.path.abspath(os.path.join(self.directory, item))
            for item in os.listdir(self.directory)
        ]
