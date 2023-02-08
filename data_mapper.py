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
import hashlib
import logging
import random
import os
from typing import AnyStr, ByteString, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MD5_LENGTH = len(hashlib.md5().digest())

def map_function(data: ByteString) -> Optional[ByteString]:
  input_length = len(data)
  max_start_index = max(0, input_length - MD5_LENGTH)
  logger.debug(f"Input Length: {input_length} | Max Write Bytes: {input_length - max_start_index}")

  if input_length == 0:
    return None

  for _ in range(0, 20):
    random_start_index = 0 if max_start_index == 0 else random.randrange(max_start_index)
    modified_segment = hashlib.md5(data).digest()
    for update_index in range(min(MD5_LENGTH, input_length)):
      data[random_start_index + update_index] = modified_segment[update_index]

  return data

def map_file(file_path: AnyStr):
  logger.debug(f"Map: {file_path}")
  with open(file_path, "rb+") as fp:
    file_data = bytearray(fp.read())
    updated_data = map_function(file_data)
    if updated_data is not None:
      fp.seek(0)
      fp.write(updated_data)

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

  if args.verbose:
    logger.setLevel(logging.DEBUG)

  # Apply map function to all files in the specified directory
  logger.info(f"Applying map function to all files in directory: {args.directory_name}")
  map_files_for_directory(args.directory_name)

if __name__ == "__main__":
    main()
