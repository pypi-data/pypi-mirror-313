from types import SimpleNamespace
import fsspec


class StorageManager:
    def __init__(self, storage_path, fs_type="file", fs_options=None):
        """
        Initializes the StorageManager with the base storage path and file system settings.
        :param storage_path: Base path for the storage.
        :param fs_type: File system type (e.g., "file", "s3").
        :param fs_options: Dictionary of options for fsspec file system (e.g., credentials).
        """
        self.storage_path = storage_path
        self.fs_type = fs_type
        self.fs_options = fs_options or {}
        self.fs = fsspec.filesystem(fs_type, **self.fs_options)
        self.depot_paths = {}
        self.depot_name = None

    @staticmethod
    def join_paths(*parts):
        """
        Joins paths using '/' as a separator, compatible with remote file systems.
        """
        return "/".join(part.strip("/") for part in parts)

    def setup_directories(self, base_path, dirs_to_create, clear_existing=False):
        """
        Creates directories using fsspec given a base path and a list of subdirectories.
        Optionally clears existing directories with safeguards.
        :param base_path: The base path where directories are created.
        :param dirs_to_create: List of subdirectories to create.
        :param clear_existing: Whether to clear existing directories.
        """
        if clear_existing:
            print(f"Warning: All existing contents in {base_path} will be removed.")
            if self.fs.exists(base_path):
                self.fs.rm(base_path, recursive=True)

        # Create the base path
        self.fs.mkdirs(base_path, exist_ok=True)

        # Create subdirectories
        for sub_directory in dirs_to_create:
            sub_path = self.join_paths(base_path, sub_directory)
            if clear_existing and self.fs.exists(sub_path):
                self.fs.rm(sub_path, recursive=True)
            self.fs.mkdirs(sub_path, exist_ok=True)

    def rebuild_depot_paths(self, depots, clear_existing=False):
        """
        Rebuilds depot_paths (dictionary) and depot_name (SimpleNamespace).
        Handles clear_existing scenario by resetting directories when required.
        :param depots: Dictionary where keys are depot names and values are subdirectory lists.
        :param clear_existing: Whether to clear existing directories.
        :return: Tuple of depot_paths (dictionary) and depot_name (SimpleNamespace).
        """
        # Ensure directories exist (optionally clear existing ones)
        for depot, sub_directories in depots.items():
            depot_path = self.join_paths(self.storage_path, depot)
            self.setup_directories(depot_path, sub_directories, clear_existing=clear_existing)

        # Generate depot_paths dictionary
        self.depot_paths = {
            depot: {sub: self.join_paths(self.storage_path, depot, sub) for sub in sub_directories}
            for depot, sub_directories in depots.items()
        }

        # Convert depot_paths to a nested SimpleNamespace
        self.depot_name = SimpleNamespace(
            **{
                depot: SimpleNamespace(**sub_dirs)
                for depot, sub_dirs in self.depot_paths.items()
            }
        )

        return self.depot_paths, self.depot_name

    def rebuild(self, depots, clear_existing=False):
        """
        Public method to clear and rebuild the depot structure.
        Calls rebuild_depot_paths internally and resets depot paths and names.
        :param depots: Dictionary where keys are depot names and values are subdirectory lists.
        :param clear_existing: Whether to clear existing directories.
        """
        print("Rebuilding depot structure...")
        self.rebuild_depot_paths(depots, clear_existing=clear_existing)
        print("Rebuild complete.")

