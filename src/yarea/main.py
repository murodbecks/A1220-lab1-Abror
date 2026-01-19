import json
import argparse
import yarea.file_io as io_mod
from yarea.gpt import extract_receipt_info

def process_directory(dirpath):
    """Processes a directory of receipt images to extract information.

    Iterates through all files in the directory, encodes them, and sends them
    to the extraction logic.

    Args:
        dirpath (str): The path to the directory containing receipt images.

    Returns:
        dict: A dictionary mapping filenames to their extracted receipt data.
    """
    results = {}
    # Iterate over files in the directory using the IO module
    for name, path in io_mod.list_files(dirpath):
        image_b64 = io_mod.encode_file(path)
        # Extract data using the GPT module
        data = extract_receipt_info(image_b64)
        results[name] = data
    return results

def main():
    """Main entry point for the receipt processing CLI application.

    Parses command-line arguments to determine the target directory and
    output format. Prints the results as JSON if the print flag is set.
    """
    # Setup command line argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("dirpath", help="Path to directory containing receipts")
    parser.add_argument("--print", action="store_true", help="Print results to stdout")
    args = parser.parse_args()

    # Process the directory and retrieve data
    data = process_directory(args.dirpath)
    
    # Output the results if requested
    if args.print:
        print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()