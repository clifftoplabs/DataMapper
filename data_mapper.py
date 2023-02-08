"""
Applies expensive map function to all files in a directory

Usage:
  data_mapper <directory_name> [-v]
  data_mapper -h | --help

Options:
  -h, --help     Show this screen.
  -v, --verbose  Verbose
"""

import argparse
import logging
import os
from typing import AnyStr

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def map_file(file_path: AnyStr):
  print(f"Map: {file_path}")

def map_files_for_directory(directory_name: AnyStr):
  for (root, _, files) in os.walk(directory_name):
    for file in files:
      map_file(os.path.join(root, file))

def main():
  # Parse the input arguments to get the run options and directory name
  arg_parser = argparse.ArgumentParser(
    prog = "data_mapper",
    description = "Applies expensive map function to all files in a directory")

  arg_parser.add_argument("directory_name")
  arg_parser.add_argument("-v", "--verbose", action="store_true")
  args = arg_parser.parse_args()

  # Apply map function to all files in the specified directory
  logger.info(f"Applying map function to all files in directory {args.directory_name}")
  map_files_for_directory(args.directory_name)

if __name__ == "__main__":
    main()
