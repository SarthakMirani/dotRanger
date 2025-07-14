#!/usr/bin/env python3

import argparse
import csv
import os
from datetime import datetime

LOG_FILE = "logs.csv"

# Ensure log file exists
def init_log_file():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "entry"])

# Command: log
def log_entry(text):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, text])
    print(f"✅ Entry added: [{timestamp}] {text}")

# Command: view
def view_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            print("📖 Health Log:")
            for row in reader:
                print(f"[{row[0]}] {row[1]}")
    else:
        print("⚠️ No entries found. Try logging something first.")

# Command: filter
def filter_logs(keyword):
    keyword = keyword.lower()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            print(f"🔎 Filtered entries for: '{keyword}'")
            found = False
            for row in reader:
                if keyword in row[1].lower():
                    print(f"[{row[0]}] {row[1]}")
                    found = True
            if not found:
                print("❌ No matching entries found.")
    else:
        print("⚠️ No entries found. Try logging something first.")

# Main CLI logic
def main():
    init_log_file()

    parser = argparse.ArgumentParser(description="🩺 careLog — CLI health journaling tool")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # log
    parser_log = subparsers.add_parser('log', help='Add a health entry')
    parser_log.add_argument('text', help='Text of the entry (in quotes)')

    # view
    subparsers.add_parser('view', help='View all logged entries')

    # filter
    parser_filter = subparsers.add_parser('filter', help='Search entries by keyword')
    parser_filter.add_argument('text', help='Keyword to search for')

    args = parser.parse_args()

    if args.command == 'log':
        log_entry(args.text)
    elif args.command == 'view':
        view_logs()
    elif args.command == 'filter':
        filter_logs(args.text)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
