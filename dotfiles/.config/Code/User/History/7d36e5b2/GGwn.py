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

def delete_by_keyword(keyword):
    if not os.path.exists(LOG_FILE):
        print("⚠️ Log file not found.")
        return

    with open(LOG_FILE, 'r') as f:
        rows = list(csv.reader(f))

    if len(rows) <= 1:
        print("⚠️ No entries found.")
        return

    header, entries = rows[0], rows[1:]
    keyword = keyword.lower()

    # Filter entries by keyword
    matches = [(i, row) for i, row in enumerate(entries) if keyword in row[1].lower()]

    if not matches:
        print(f"❌ No entries found containing: '{keyword}'")
        return

    print(f"🔍 Found {len(matches)} matching entries for '{keyword}':\n")
    for i, (real_index, row) in enumerate(matches, start=1):
        print(f"{i}. [{row[0]}] {row[1]}")

    try:
        choice = int(input(f"\n❓ Delete which one? (1-{len(matches)}): "))
        if 1 <= choice <= len(matches):
            # Delete the chosen entry from original entries
            del_index = matches[choice - 1][0]
            deleted = entries.pop(del_index)

            # Write updated entries
            with open(LOG_FILE, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(entries)

            print(f"\n🗑️ Deleted entry: [{deleted[0]}] {deleted[1]}")
        else:
            print("⚠️ Invalid choice. No entry deleted.")
    except ValueError:
        print("⚠️ Invalid input. Please enter a number.")

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

    # delete (interactive only)
    parser_delete = subparsers.add_parser('delete', help='Search and delete a log entry by keyword')
    parser_delete.add_argument('keyword', help='Keyword to filter and choose entry to delete')


    args = parser.parse_args()

    if args.command == 'log':
        log_entry(args.text)
    elif args.command == 'view':
        view_logs()
    elif args.command == 'filter':
        filter_logs(args.text)
    elif args.command == 'delete':
        delete_by_keyword(args.keyword)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
