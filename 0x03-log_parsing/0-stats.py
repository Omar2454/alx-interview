#!/usr/bin/python3
"""
This script reads standard input for log entries, computes and prints metrics.
It handles logs formatted as: <IP Address> - [<date>] "GET /projects/260 HTTP/1.1" <status code> <file size>
It computes the total file size and counts of occurrences of each HTTP status code after every 10 lines or upon keyboard interruption.
"""

import sys
import re
import signal

def print_statistics(total_file_size, status_counts):
    print("File size: {}".format(total_file_size))
    for status in sorted(status_counts.keys()):
        if status_counts[status] > 0:
            print("{}: {}".format(status, status_counts[status]))

def signal_handler(signal, frame):
    print_statistics(total_file_size, status_codes)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Initialize counters
total_file_size = 0
status_codes = {200: 0, 301: 0, 400: 0, 401: 0, 403: 0, 404: 0, 405: 0, 500: 0}
line_count = 0

# Regex to match the log format
log_pattern = re.compile(r'^\d+\.\d+\.\d+\.\d+ - \[\S+?\] "GET /projects/260 HTTP/1\.1" (\d{3}) (\d+)$')

# Process each line from standard input
for line in sys.stdin:
    match = log_pattern.search(line)
    if match:
        status_code = int(match.group(1))
        file_size = int(match.group(2))

        if status_code in status_codes:
            status_codes[status_code] += 1
            total_file_size += file_size
            line_count += 1

            if line_count == 10:
                print_statistics(total_file_size, status_codes)
                line_count = 0

# If the process is ended without an interruption and there are fewer than 10 lines
if line_count > 0:
    print_statistics(total_file_size, status_codes)
