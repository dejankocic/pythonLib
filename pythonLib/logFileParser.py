#This is a sample script for checking the reg exp. In general should be ignored (no value).
#

import re

log_pattern = re.compile(r'(?P<LogLevel>\w+)\s+(?P<Timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3})\s+\[(?P<Thread>[^\]]+)\]:\s(?P<Logger>[^\s]+)\s-\s(?P<Message>.+)')

log_entries = [
    "INFO  2024-03-10 09:31:51.967 [JavaBridge]: com.ug.eon.android.tv.networkcheck.NetworkHelper - Is device connected through Wi-Fi - true",
    "TRACE 2024-03-10 09:31:51.970 [AsyncTask #150]: com.ug.eon.android.tv.web.BatchFileDownloadTask - File exists, skipping download: /data/user/0/com.ug.eon.android.tv/cache/images/2021/11/09/09/56/07/s_dark_480x270.png",
    "TRACE 2024-03-10 09:31:51.970 [AsyncTask #150]: com.ug.eon.android.tv.web.BatchFileDownloadTask - File exists, skipping download: /data/user/0/com.ug.eon.android.tv/cache/images/2021/11/09/09/56/07/stb_fhd_dark_480x270.png"
]

for entry in log_entries:
    match = log_pattern.match(entry)
    if match:
        print(f"Log Level: {match.group('LogLevel')}")
        print(f"Timestamp: {match.group('Timestamp')}")
        print(f"Thread: {match.group('Thread')}")
        print(f"Logger: {match.group('Logger')}")
        print(f"Message: {match.group('Message')}")
        print()
