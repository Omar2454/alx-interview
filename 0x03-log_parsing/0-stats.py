#!/usr/bin/python3
"""
Reads standard input line by line to process log data formatted as:
<IP Address> - [<date>] "GET /projects/260 HTTP/1.1" <status code> <file size>
It skips lines that don't match the format and tallies results every 10 lines or on keyboard interruption.
"""

import sys

def print_statistics(file_size, status_counts):
    print("File size: {}".format(file_size))
    for status in sorted(status_counts.keys()):
        if status_counts[status] > 0:
            print("{}: {}".format(status, status_counts[status]))

def main():
    import signal
    import re

    # Handling keyboard interrupt to ensure statistics are printed before the program exits
    def signal_handler(sig, frame):
        print_statistics(total_file_size, status_codes)
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    total_file_size = 0
    status_codes = {200: 0, 301: 0, 400: 0, 401: 0, 403: 0, 404: 0, 405: 0, 500: 0}
    line_count = 0

    log_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - \[\S+?\] "GET /projects/260 HTTP/1\.1" (\d{3}) (\d+)')
    
    for line in sys.stdin:
        match = log_pattern.match(line)
        if match:
            line_count += 1
            total_file_size += int(match.group(3))
            status_code = int(match.group(2))
            if status_code in status_codes:
                status_codes[status_code] += 1
            
            if line_count == 10:
                print_statistics(total_file_size, status_codes)
                line_count = 0  # reset line count after printing

    # In case total line count isn't a multiple of 10
    if line_count != 0:
        print_statistics(total_file_size, status_codes)

if __name__ == "__main__":
    main()
