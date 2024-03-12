import os
import re
import zipfile
import tempfile
import sys
from collections import defaultdict

def unpack_zip(file_path, extract_to):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        for file in zip_ref.namelist():
            if file.endswith('.zip'):
                unpack_zip(os.path.join(extract_to, file), extract_to)

def find_log_files_and_count_loggers(start_path):
    logger_pattern = re.compile(
        r'(?P<LogLevel>\w+)\s+(?P<Timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3})\s+\[(?P<Thread>[^\]]+)\]:\s(?P<Logger>[^\s]+)\s-\s(?P<Message>.+)')

    loggers = defaultdict(int)
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
                                    logger = match.group('Logger')
                                    loggers[logger] += 1
                        break
                    except UnicodeDecodeError:
                        continue
    return loggers

def main():
    log_directory = input("Enter the full path of the directory to check logs: ")
    if not os.path.isdir(log_directory):
        print("The provided directory does not exist. Please check the path and try again.")
        sys.exit(1)

    zip_files = [file for file in os.listdir(log_directory) if file.endswith('.zip')]
    all_loggers = defaultdict(int)

    for zip_file in zip_files:
        print(f"Processing {zip_file}...")
        temp_dir = tempfile.mkdtemp(dir=log_directory)
        unpack_zip(os.path.join(log_directory, zip_file), temp_dir)
        loggers = find_log_files_and_count_loggers(temp_dir)
        for logger, count in loggers.items():
            all_loggers[logger] += count

    with open('summary_results.txt', 'w') as f:
        for logger, count in sorted(all_loggers.items(), key=lambda item: item[1], reverse=True):
            f.write(f"{logger}: {count}\n")

    print("Summary of found loggers has been written to 'summary_results.txt'.")

if __name__ == "__main__":
    main()
