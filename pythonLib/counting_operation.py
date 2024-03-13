import os
import re
from collections import defaultdict

def find_log_files_and_count(start_path, count_option):
    logger_pattern = re.compile(
        r'(?P<LogLevel>\w+)\s+(?P<Timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3})\s+\[(?P<Thread>[^\]]+)\]:\s(?P<Logger>[^\s]+)\s-\s(?P<Message>.+)')

    counts = defaultdict(lambda: defaultdict(int))
    file_counts = defaultdict(set)

    encodings = ['utf-8', 'utf-16-le', 'utf-16-be', 'cp1252']

    for root, dirs, files in os.walk(start_path):
        for file in files:
            if file.endswith('.log'):
                print(f"Processing {file}...")  # Print the currently processed .log file
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
                                    if file not in ['EonQoE.log', 'EonQoS.log'] or match.group('LogLevel') in ['ERROR', 'FATAL', 'WARN']:
                                        counts[key][file] += 1
                                        file_counts[key].add(file)
                        break
                    except UnicodeDecodeError:
                        continue
    return counts, file_counts
