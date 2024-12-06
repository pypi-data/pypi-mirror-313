import os


__all__ = [
    "get_user_input",
    "get_directory",
    "get_filename",
    "get_file_path"
    ]


def get_user_input(prompt: str, type_func=str):
    """
    Helper function to get input from the user and convert it to
    the desired type.
    Args:
        prompt (str): The prompt to display to the user.
        type_func (type): The type to convert the input to.
    """
    while True:
        try:
            user_input = input(prompt)
            return type_func(user_input)
        except ValueError:
            print(f"Invalid input. Please enter a valid {type_func.__name__}.")


def get_directory(prompt: str):
    """
    Prompts the user for a directory path and checks if it exists.
    Repeats the prompt until a valid directory is provided.
    Args:
        prompt (str): The prompt to display to the user.
    """
    while True:
        directory = input(prompt)
        if os.path.isdir(directory):
            return directory
        else:
            print("Invalid directory.")
            print("Please enter a valid path to an existing directory.")


def get_filename(prompt: str):
    """
    Prompts the user for a filename.
    Ensures the filename does not contain invalid characters.
    Args:
        prompt (str): The prompt to display to the user.
    """
    while True:
        filename = input(prompt)
        if any(char in filename for char in r'<>:"/\|?*'):
            print("Invalid filename. Please avoid characters: <>:\"/\\|?*")
        else:
            return filename


def get_file_path(prompt: str):
    """
    Prompts the user for a file path and checks if the file exists.
    Repeats the prompt until a valid file path is provided.
    Args:
        prompt (str): The prompt to display to the user.
    """
    while True:
        file_path = input(prompt)
        if os.path.isfile(file_path):
            return file_path
        else:
            print("Invalid file path.")
            print("Please enter a valid path to an existing file.")
