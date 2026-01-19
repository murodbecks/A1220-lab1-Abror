import os
import base64

def encode_file(path):
    """Reads a file from disk and encodes it as a base64 string.

    Args:
        path (str): The file path to the image to be encoded.

    Returns:
        str: The UTF-8 decoded base64 string representation of the file content.
    """
    # Open the file in binary read mode and encode content
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def list_files(dirpath):
    """Yields filenames and full paths for all files in a directory.

    Args:
        dirpath (str): The path to the directory to traverse.

    Yields:
        tuple: A tuple containing (filename, full_path) for each file found.
    """
    # Iterate through all entries in the given directory
    for name in os.listdir(dirpath):
        path = os.path.join(dirpath, name)
        # Check if the entry is a file before yielding
        if os.path.isfile(path):
            yield name, path