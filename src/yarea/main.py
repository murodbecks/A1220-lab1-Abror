# main.py
import json
import argparse
import yarea.file_io as io_mod
from yarea.gpt import extract_receipt_info

def process_directory(dirpath):
    results = {}
    for name, path in io_mod.list_files(dirpath):
        image_b64 = io_mod.encode_file(path)
        data = extract_receipt_info(image_b64)
        results[name] = data
    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dirpath")
    parser.add_argument("--print", action="store_true")
    args = parser.parse_args()

    data = process_directory(args.dirpath)
    if args.print:
        print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()

