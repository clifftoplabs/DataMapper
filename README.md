# Data Mapper
Tool to apply expensive map function to all files in a directory

## Run
You can run the tool with the following command:
```
python3 data_mapper.py example_directory
```

You can can also see a full list of options by looking at the help documentation:
```
python3 data_mapper.py [-h | --help]
```

### Example Output
```
-> % python3 data_mapper.py example_directory
INFO:__main__:Applying map function to all files in directory: example_directory
INFO:__main__:Completed mapping of 500.0027 MB in 2.8928 sec with 0.1728 GB/s throughput.

-> % python3 data_mapper.py example_directory -s
INFO:__main__:Applying map function to all files in directory: example_directory
INFO:__main__:Completed mapping of 500.0027 MB in 12.6360 sec with 0.0396 GB/s throughput.
```

## File Generator

Tool to generate files of specified length in bytes.

### Run
You can run the tool with the following command:
```
python3 file_generator.py 100 example_directory/very_large_file.txt
```
