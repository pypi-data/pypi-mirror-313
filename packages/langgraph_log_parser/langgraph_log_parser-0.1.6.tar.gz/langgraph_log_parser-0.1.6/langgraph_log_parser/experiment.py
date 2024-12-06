import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class ExperimentPaths:
    """
    Class that holds and manages all paths for an experiment.

    :param name: Name of the experiment that will be used for folder structure.
    :type name: str
    :param base_dir: Base directory where all experiments are stored, defaults to "experiments".
    :type base_dir: str
    """
    name: str
    base_dir: str = "experiments"

    @property
    def database(self) -> str:
        """
        Returns path to the main SQLite database.

        :return: Full path to the SQLite database file.
        :rtype: str

        **Example:**

        >>> paths = ExperimentPaths("test")
        >>> paths.database
        'experiments/test/db/test.sqlite'
        """
        return os.path.join(self.base_dir, self.name, "db", f"{self.name}.sqlite")

    @property
    def json_dir(self) -> str:
        """
        Returns path to the json directory.

        :return: Full path to the JSON directory.
        :rtype: str

        **Example:**

        >>> paths = ExperimentPaths("test")
        >>> paths.json_dir
        'experiments/test/json'
        """
        return os.path.join(self.base_dir, self.name, "json")

    @property
    def csv_dir(self) -> str:
        """
        Returns path to the csv directory.

        :return: Full path to the CSV directory.
        :rtype: str

        **Example:**

        >>> paths = ExperimentPaths("test")
        >>> paths.csv_dir
        'experiments/test/csv'
        """
        return os.path.join(self.base_dir, self.name, "csv")

    @property
    def img_dir(self) -> str:
        """
        Returns path to the img directory.

        :return: Full path to the images directory.
        :rtype: str

        **Example:**

        >>> paths = ExperimentPaths("test")
        >>> paths.img_dir
        'experiments/test/img'
        """
        return os.path.join(self.base_dir, self.name, "img")

    @property
    def reports_dir(self) -> str:
        """
        Returns path to the reports directory.

        :return: Full path to the reports directory.
        :rtype: str

        **Example:**

        >>> paths = ExperimentPaths("test")
        >>> paths.reports_dir
        'experiments/test/reports'
        """
        return os.path.join(self.base_dir, self.name, "reports")

    @property
    def reports_all_dir(self) -> str:
        """
        Returns path to the reports/all directory.

        :return: Full path to the reports/all directory.
        :rtype: str

        **Example:**

        >>> paths = ExperimentPaths("test")
        >>> paths.reports_all_dir
        'experiments/test/reports/all'
        """
        return os.path.join(self.reports_dir, "all")

    @property
    def reports_cases_dir(self) -> str:
        """
        Returns path to the reports/cases directory.

        :return: Full path to the reports/cases directory.
        :rtype: str

        **Example:**

        >>> paths = ExperimentPaths("test")
        >>> paths.reports_cases_dir
        'experiments/test/reports/cases'
        """
        return os.path.join(self.reports_dir, "cases")

    def get_csv_path(self, filename: str = "csv_output.csv") -> str:
        """
        Returns full path for a CSV file.

        :param filename: Name of the CSV file.
        :type filename: str
        :return: Full path to the CSV file.
        :rtype: str

        **Example:**

        >>> paths = ExperimentPaths("test")
        >>> paths.get_csv_path("data.csv")
        'experiments/test/csv/data.csv'
        """
        return os.path.join(self.csv_dir, filename)

    def get_img_path(self, filename: Optional[str] = None) -> str:
        """
        Returns full path for an image file.

        :param filename: Name of the image file, if None uses the default from the calling function
        :type filename: Optional[str]
        :return: Full path to the image file.
        :rtype: str

        **Example:**

        >>> paths = ExperimentPaths("test")
        >>> paths.get_img_path("plot.png")
        'experiments/test/img/plot.png'
        >>> # When used in functions, will use that function's default
        >>> generate_prefix_tree(event_log, paths.get_img_path())  # Will use 'tree.png'
        >>> generate_dfg(event_log, paths.get_img_path())  # Will use 'dfg.png'
        """
        if filename is None:
            return self.img_dir
        return os.path.join(self.img_dir, filename)


def _create_folder_structure(folder_name: str) -> None:
    """
    Create a folder structure inside 'experiments' directory with db, img, json, csv, and reports subfolders.

    :param folder_name: Name of the main folder to be created inside experiments directory.
    :type folder_name: str

    **Example:**

    >>> _create_folder_structure("test_directory")
    Successfully created 'experiments/test_directory' with subfolders: db, img, json, csv, reports/all, reports/cases
    """
    # Define experiments directory
    experiments_dir = "experiments"

    # Create experiments directory if it doesn't exist
    if not os.path.exists(experiments_dir):
        os.makedirs(experiments_dir)

    # Full path for the main folder
    full_path = os.path.join(experiments_dir, folder_name)

    # Check if folder exists
    if os.path.exists(full_path):
        raise FileExistsError(f"Error: Folder '{full_path}' already exists!")

    try:
        # Create main folder inside experiments
        os.makedirs(full_path)

        # Create all subfolders
        basic_subfolders = ['db', 'img', 'json', 'csv', 'reports']
        for subfolder in basic_subfolders:
            subfolder_path = os.path.join(full_path, subfolder)
            os.makedirs(subfolder_path)

            # Create reports subdirectories
            if subfolder == 'reports':
                os.makedirs(os.path.join(subfolder_path, 'all'))
                os.makedirs(os.path.join(subfolder_path, 'cases'))

        print(
            f"Successfully created '{full_path}' with subfolders: {', '.join(basic_subfolders[:-1])}, reports/all, reports/cases")

    except OSError as error:
        print(f"Error creating folder structure: {error}")


def create_experiment(name: str) -> ExperimentPaths:
    """
    Main function to set up experiment and return paths. This is the main entry point
    for creating a new experiment structure.

    :param name: Name of the experiment to be created.
    :type name: str
    :return: ExperimentPaths object containing all relevant paths.
    :rtype: ExperimentPaths

    **Example:**

    >>> paths = create_experiment("my_experiment")
    Creating new experiment...
    Successfully created 'experiments/my_experiment' with subfolders: db, img, json, csv
    Experiment 'my_experiment' created successfully!
    Database path: experiments/my_experiment/db/my_experiment.sqlite
    JSON directory: experiments/my_experiment/json
    CSV directory: experiments/my_experiment/csv
    Image directory: experiments/my_experiment/img
    Reports directory: experiments/my_experiment/reports
    - All reports: experiments/my_experiment/reports/all
    - Case reports: experiments/my_experiment/reports/cases
    """
    print("\nCreating new experiment...")
    _create_folder_structure(name)
    paths = ExperimentPaths(name)

    print(f"\nExperiment '{paths.name}' created successfully!")
    print(f"Database path: {paths.database}")
    print(f"JSON directory: {paths.json_dir}")
    print(f"CSV directory: {paths.csv_dir}")
    print(f"Image directory: {paths.img_dir}")
    print(f"Reports directory: {paths.reports_dir}")
    print(f"- All reports: {paths.reports_all_dir}")
    print(f"- Case reports: {paths.reports_cases_dir}")
    return paths