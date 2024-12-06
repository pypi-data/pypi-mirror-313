class SwatAquiferDeepRemoval:
    """Copy all content to a new csv file, except all lines that contains '_deep'.

    The files are handled as normal text files, and the content is copied line by line.
    The cleaned file can be read using a csv reader afterwards.
    """

    def __init__(self, csv_original_path: str, csv_cleaned_path: str):
        """Instantiates a SwatAquiferDeepRemoval object.

        Parameters:
        - csv_original_path (str): The path to the original CSV file.
        - csv_cleaned_path (str): The path to the cleaned CSV file.
        """
        self.csv_original_path: str = csv_original_path
        self.csv_cleaned_path: str = csv_cleaned_path

    def clean(self):
        """Copy line by line from the original CSV file to the cleaned CSV file, except lines containing '_deep'."""

        with open(self.csv_original_path, "r") as original_file, open(
            self.csv_cleaned_path, "w"
        ) as cleaned_file:
            for line in original_file:
                if "_deep" not in line:
                    cleaned_file.write(line)
