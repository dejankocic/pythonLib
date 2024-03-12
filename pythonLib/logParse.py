import os
import re
import zipfile
import tempfile
import sys


def unpack_zip(file_path, extract_to):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        for file in zip_ref.namelist():
            if file.endswith('.zip'):
                unpack_zip(os.path.join(extract_to, file), extract_to)


def find_log_files_and_count_loggers(start_path):
    logger_pattern = re.compile(
        r'^\\w+\\s+\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}\\.\\d{3} \\[\\w+\\]: ([^ ]+) - .+$')
    loggers = {}
    # Add 'utf-16-le' and 'utf-16-be' to the list of encodings to try
    encodings = ['utf-8', 'utf-16', 'utf-16-le', 'utf-16-be', 'cp1252']

    for root, dirs, files in os.walk(start_path):
        for file in files:
            if file.endswith('.log'):
                for encoding in encodings:
                    try:
                        with open(os.path.join(root, file), 'r', encoding=encoding) as log_file:
                            for line in log_file:
                                match = logger_pattern.match(line)
                                if match:
                                    logger = match.group(1)
                                    if logger in loggers:
                                        loggers[logger] += 1
                                    else:
                                        loggers[logger] = 1
                        # If the file is successfully read, break out of the encoding loop
                        break
                    except UnicodeDecodeError:
                        # If an error occurs, try the next encoding
                        continue
    return loggers


def main():
    current_dir = os.getcwd()
    zip_files = [file for file in os.listdir(current_dir) if file.endswith('.zip')]

    for zip_file in zip_files:
        print(f"Processing {zip_file}...")
        temp_dir = tempfile.mkdtemp(dir=current_dir)
        unpack_zip(zip_file, temp_dir)
        loggers = find_log_files_and_count_loggers(temp_dir)

        print("Temporary directory created at:", temp_dir)
        print("List of found loggers:")
        for logger, count in sorted(loggers.items()):
            print(f"{logger}: {count}")

        print("Press Enter to continue to the next file.")
        input()  # Wait for user input before continuing


if __name__ == "__main__":
    main()
