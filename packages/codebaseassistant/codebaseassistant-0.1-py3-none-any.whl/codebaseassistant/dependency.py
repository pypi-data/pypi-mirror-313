class Dependency:
    def __init__(self, file_path, imported_items=None, is_external=False):
        """
        Represents a dependency within a codebase.

        :param file_path: Path to the file being imported or module name (e.g., 'os' for built-ins).
        :param imported_items: List of specific items (e.g., functions, classes, variables) imported from the file.
        :param is_external: Indicates if the dependency is external (e.g., built-in modules or external libraries).
        """
        self.file_path = file_path
        self.imported_items = imported_items or []
        self.is_external = is_external

    def serialize(self):
        """
        Converts the Dependency object into a dictionary for saving to a file.

        :return: A serialized representation of the Dependency.
        """
        return {
            "file_path": self.file_path,
            "imported_items": self.imported_items,
            "is_external": self.is_external
        }

    @staticmethod
    def unserialize(data):
        """
        Recreates a Dependency object from a serialized representation.

        :param data: A dictionary representation of a Dependency.
        :return: A Dependency object.
        """
        return Dependency(
            file_path=data["file_path"],
            imported_items=data.get("imported_items", []),
            is_external=data.get("is_external", False)
        )

    def __repr__(self):
        return (f"Dependency(file_path='{self.file_path}', "
                f"imported_items={self.imported_items}, is_external={self.is_external})")
