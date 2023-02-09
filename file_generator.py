"""
Generates file of arbitrary length in bytes

Usage:
  file_generator <total_mb> <output_file>
  file_generator -h | --help

Options:
  -h, --help     Show this screen.
"""

import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
  # Parse the input arguments to get the run options and directory name
  arg_parser = argparse.ArgumentParser(
    prog = "file_generator",
    description = "Generates file of arbitrary length in bytes")

  arg_parser.add_argument("total_mb")
  arg_parser.add_argument("output_file")
  args = arg_parser.parse_args()

  total_bytes = int(float(args.total_mb) * 1000. * 1000.)

  # Apply map function to all files in the specified directory
  logger.info(f"Printing {total_bytes:,d} bytes to {args.output_file}")
  with open(args.output_file, "w+") as fp:
    fp.write(bytearray(total_bytes).decode("utf-8"))

if __name__ == "__main__":
    main()
