"""
Applies expensive map function to all files in a directory

Usage:
  data_mapper <directory_name> [-v] [-s]
  data_mapper -h | --help

Options:
  -s, --serial   Run in a single thread
  -h, --help     Show this screen.
  -v, --verbose  Verbose
"""

import argparse
import hashlib
import logging
import os
import random
from threading import Thread, Lock
import time
from typing import AnyStr, ByteString, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MD5_LENGTH = len(hashlib.md5().digest())

class FileAccumulator:
  def __init__(self, run_serially: bool):
    self.run_serially = run_serially
    self.total_bytes = 0
    self.start_time = time.time()
    self._lock = None if run_serially else Lock()

  def add_file_data(self, data: ByteString):
    if not self.run_serially:
      self._lock.acquire()

    self.total_bytes += len(data)

    if not self.run_serially:
      self._lock.release()

  def get_elapsed_time(self):
    return time.time() - self.start_time

  def get_total_gigabytes(self):
    return self.total_bytes / (1000. * 1000. * 1000.)

  def get_throughput(self):
    current_gb = self.get_total_gigabytes()
    elapsed_time_s = self.get_elapsed_time()
    # Return in GB/sec
    return current_gb / elapsed_time_s


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

def map_file(file_path: AnyStr, accumulator: FileAccumulator):
  logger.debug(f"Map: {file_path}")
  with open(file_path, "rb+") as fp:
    file_data = bytearray(fp.read())
    accumulator.add_file_data(file_data)
    updated_data = map_function(file_data)
    if updated_data is not None:
      fp.seek(0)
      fp.write(updated_data)

def map_files_for_directory(directory_name: AnyStr, run_serially: bool):
  threads = []
  accumulator = FileAccumulator(run_serially)
  for (root, _, files) in os.walk(directory_name):
    for file in files:
      file_path = os.path.join(root, file)
      if run_serially:
        map_file(file_path, accumulator)
      else:
        thread = Thread(target=map_file, args=(file_path, accumulator))
        thread.start()
        threads.append(thread)

  for thread in threads:
    thread.join()

  throughput = accumulator.get_throughput()
  total_mb = accumulator.get_total_gigabytes() * 1000.
  total_time = accumulator.get_elapsed_time()
  logger.info(f"Completed mapping of {total_mb:.4f} MB in {total_time:.4f} sec with {throughput:.4f} GB/s throughput.")


def main():
  # Parse the input arguments to get the run options and directory name
  arg_parser = argparse.ArgumentParser(
    prog = "data_mapper",
    description = "Applies expensive map function to all files in a directory")

  arg_parser.add_argument("directory_name")
  arg_parser.add_argument("-v", "--verbose", action="store_true")
  arg_parser.add_argument("-s", "--serial", action="store_true")
  args = arg_parser.parse_args()

  if args.verbose:
    logger.setLevel(logging.DEBUG)

  # Apply map function to all files in the specified directory
  logger.info(f"Applying map function to all files in directory: {args.directory_name}")
  map_files_for_directory(args.directory_name, args.serial)

if __name__ == "__main__":
    main()
