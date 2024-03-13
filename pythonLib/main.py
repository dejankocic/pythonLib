import os
import zipfile
import tempfile
import sys
from collections import defaultdict
import shutil
import csv
from counting_operation import find_log_files_and_count  # Import the function from the new script

def unpack_zip(file_path, extract_to):
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
            for file in zip_ref.namelist():
                if file.endswith('.zip'):
                    unpack_zip(os.path.join(extract_to, file), extract_to)
    except zipfile.BadZipFile:
        print(f"Error: {file_path} is not a zip file.")
        with open('unprocessed_in_error.txt', 'a') as error_file:
            error_file.write(f"{file_path}\\n")  # Add a newline character after each file path

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
    all_file_counts = defaultdict(set)

    for zip_file in zip_files:
        print(f"Processing {zip_file}...")
        temp_dir = tempfile.mkdtemp(dir=log_directory)
        unpack_zip(os.path.join(log_directory, zip_file), temp_dir)
        counts, file_counts = find_log_files_and_count(temp_dir, count_option)
        for key, count in counts.items():
            all_counts[key] += sum(count.values())
            all_file_counts[key].update(file_counts[key])
        shutil.rmtree(temp_dir)  # Delete the temporary directory after processing

    with open('summary_results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Option", "Count", "Files"])
        for key, count in sorted(all_counts.items(), key=lambda item: item[1], reverse=True):
            writer.writerow([key, count, ', '.join(all_file_counts[key])])

    print("Summary has been written to 'summary_results.csv'.")

if __name__ == "__main__":
    main()
