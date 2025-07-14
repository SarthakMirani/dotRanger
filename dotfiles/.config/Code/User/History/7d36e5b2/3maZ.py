#!/usr/bin/env python3

import argparse
import csv
from datetime import datetime
import os

LOG_FILE = "logs.csv"

# Create the CSV if it doesn't exist
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "entry"])

def main():
    parser = argparse.ArgumentParser(description="🩺 careLog — CLI health journaling tool")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # log command
    parser_log = subparsers.add_parser('log', help='Add a health entry')
    parser_log.add_argument('text', help='Text of the entry, in quotes')

    # view command
    subparsers.add_parser('view', help='View all health entries')

    # filter command
    parser_filter = subparsers.add_parser('filter', help='Search entries by keyword')
    parser_filter.add_argument('text', help='Keyword to search for')

    args = parser.parse_args()

    # log
    if args.command == 'log':
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, args.text])
        print(f"✅ Entry added: [{timestamp}] {args.text}")

    # view
    elif args.command == 'view':
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                reader = csv.reader(f)
                next(reader)
                print("📖 Health Log:")
                for row in reader:
                    print(f"[{row[0]}] {row[1]}")
        else:
            print("⚠️ No entries found. Try logging something first.")

    # filter
    elif args.command == 'filter':
        keyword = args.text.lower()
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                reader = csv.reader(f)
                next(reader)
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

    else:
        parser.print_help()
