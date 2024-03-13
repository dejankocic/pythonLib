#The script for a given directory iterates in archives and searches for .log files,
# so it counts what has been selected (loggers, log levels, messages).

import os
import re
import zipfile
import tempfile
import sys
from collections import defaultdict
import shutil

def unpack_zip(file_path, extract_to):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        for file in zip_ref.namelist():
            if file.endswith('.zip'):
                unpack_zip(os.path.join(extract_to, file), extract_to)

def find_log_files_and_count(start_path, count_option):
    logger_pattern = re.compile(
        r'(?P<LogLevel>\w+)\s+(?P<Timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3})\s+\[(?P<Thread>[^\]]+)\]:\s(?P<Logger>[^\s]+)\s-\s(?P<Message>.+)')

    counts = defaultdict(int)
    encodings = ['utf-8', 'utf-16-le', 'utf-16-be', 'cp1252']

    for root, dirs, files in os.walk(start_path):
        for file in files:
            if file.endswith('.log'):
                for encoding in encodings:
                    try:
                        with open(os.path.join(root, file), 'r', encoding=encoding) as log_file:
                            for line in log_file:
                                match = logger_pattern.search(line)
                                if match:
                                    if count_option == 1:
                                        key = match.group('LogLevel')
                                    elif count_option == 2:
                                        key = match.group('Logger')
                                    elif count_option == 3:
                                        key = match.group('Message')
                                    counts[key] += 1
                        break
                    except UnicodeDecodeError:
                        continue
    return counts

def main():
    log_directory = input("Enter the full path of the directory to check logs: ")
    if not os.path.isdir(log_directory):
        print("The provided directory does not exist. Please check the path and try again.")
        sys.exit(1)

    print("Select what to count:")
    print("1: Log Levels")
    print("2: Loggers")
    print("3: Messages")
    count_option = int(input("Enter your selection (1, 2, or 3): "))

    zip_files = [file for file in os.listdir(log_directory) if file.endswith('.zip')]
    all_counts = defaultdict(int)

    for zip_file in zip_files:
        print(f"Processing {zip_file}...")
        temp_dir = tempfile.mkdtemp(dir=log_directory)
        unpack_zip(os.path.join(log_directory, zip_file), temp_dir)
        counts = find_log_files_and_count(temp_dir, count_option)
        for key, count in counts.items():
            all_counts[key] += count
        shutil.rmtree(temp_dir)  # Delete the temporary directory after processing

    with open('summary_results.txt', 'w', encoding='utf-8') as f:
        for key, count in sorted(all_counts.items(), key=lambda item: item[1], reverse=True):
            f.write(f"{key}: {count}\n")

    print("Summary has been written to 'summary_results.txt'.")

if __name__ == "__main__":
    main()
