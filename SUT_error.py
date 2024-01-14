import os
from messagebox.CTkMessagebox import CTkMessagebox


def check_empty_file(file_name, directory):
    """Check if the folder or file is empty"""
    if not file_name:  # Check if the folder is empty
        CTkMessagebox(title="Error", message="Your folder is empty", icon="cancel", fade_in_duration=0.2)
        return False
    # Rest of your code to check for empty files
    return True


def extract_directory_path(file_path):
    """
    This function extracts the directory path without the file name and extension.

    Args:
    file_path (str): The full file path including the file name and extension.

    Returns:
    str: The directory path without the file name and extension.
    """
    directory_path = os.path.dirname(file_path)  # Extract the directory path
    return directory_path


def extract_file_name(file_path):
    """
    This function extracts the file name from the file path.

    Args:
    file_path (str): The full file path including the file name and extension.

    Returns:
    str: The file name without the directory path and extension.
    """

    file_name = os.path.basename(file_path)  # Extract the file name
    return file_name



class EmptyFileError(Exception):
    """Return's the empty file error"""
