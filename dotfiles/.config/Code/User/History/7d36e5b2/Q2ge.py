#!/usr/bin/env python3

import argparse
import csv
import os
from datetime import datetime
from collections import Counter
import json

LOG_FILE = "logs.csv"

# Ensure log file exists and has header
def init_log_file():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "entry", "tag"])

# Command: log
def log_entry(text, tag):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, text, tag or ""])
    print(f"✅ Entry added: [{timestamp}] {text} ({tag or 'no tag'})")

# Command: view
def view_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            print("📖 Health Log:")
            for row in reader:
                print(f"[{row[0]}] {row[1]} ({row[2]})")
    else:
        print("⚠️ No entries found. Try logging something first.")

# Command: filter
def filter_logs(keyword=None, tag=None):
    keyword = keyword.lower() if keyword else None
    tag = tag.lower() if tag else None

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            print("🔎 Filtered entries:")
            found = False
            for row in reader:
                if ((not keyword or keyword in row[1].lower()) and
                    (not tag or tag == row[2].lower())):
                    print(f"[{row[0]}] {row[1]} ({row[2]})")
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

    matches = [(i, row) for i, row in enumerate(entries) if keyword in row[1].lower()]

    if not matches:
        print(f"❌ No entries found containing: '{keyword}'")
        return

    print(f"🔍 Found {len(matches)} matching entries for '{keyword}':\n")
    for i, (real_index, row) in enumerate(matches, start=1):
        print(f"{i}. [{row[0]}] {row[1]} ({row[2]})")

    try:
        choice = int(input(f"\n❓ Delete which one? (1-{len(matches)}): "))
        if 1 <= choice <= len(matches):
            del_index = matches[choice - 1][0]
            deleted = entries.pop(del_index)

            with open(LOG_FILE, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(entries)

            print(f"\n🗑️ Deleted entry: [{deleted[0]}] {deleted[1]} ({deleted[2]})")
        else:
            print("⚠️ Invalid choice. No entry deleted.")
    except ValueError:
        print("⚠️ Invalid input. Please enter a number.")

def edit_entry(keyword):
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

    matches = [(i, row) for i, row in enumerate(entries) if keyword in row[1].lower()]

    if not matches:
        print(f"❌ No entries found containing: '{keyword}'")
        return

    print(f"🔍 Found {len(matches)} matching entries for '{keyword}':\n")
    for i, (real_index, row) in enumerate(matches, start=1):
        print(f"{i}. [{row[0]}] {row[1]} ({row[2]})")

    try:
        choice = int(input(f"\n❓ Edit which one? (1-{len(matches)}): "))
        if 1 <= choice <= len(matches):
            edit_index = matches[choice - 1][0]
            old_entry = entries[edit_index]

            new_text = input(f"📝 New text for [{old_entry[0]}] {old_entry[1]}\n> ").strip()
            new_tag = input(f"🏷️  New tag (leave blank to keep '{old_entry[2]}'): ").strip()
            if not new_text:
                print("⚠️ Empty input. Entry not changed.")
                return

            entries[edit_index] = [old_entry[0], new_text, new_tag or old_entry[2]]

            with open(LOG_FILE, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(entries)

            print(f"\n✅ Updated entry: [{old_entry[0]}] {new_text} ({new_tag or old_entry[2]})")
        else:
            print("⚠️ Invalid choice. No entry edited.")
    except ValueError:
        print("⚠️ Invalid input. Please enter a number.")

def export_logs(format):
    if not os.path.exists(LOG_FILE):
        print("⚠️ Log file not found.")
        return

    with open(LOG_FILE, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    if len(rows) <= 1:
        print("⚠️ No entries to export.")
        return

    header, entries = rows[0], rows[1:]

    if format == 'txt':
        with open('export.txt', 'w') as f:
            for row in entries:
                f.write(f"[{row[0]}] {row[1]} ({row[2]})\n")
        print("📄 Logs exported to export.txt")

    elif format == 'json':
        data = [{"timestamp": row[0], "entry": row[1], "tag": row[2]} for row in entries]
        with open('export.json', 'w') as f:
            json.dump(data, f, indent=4)
        print("📄 Logs exported to export.json")

def show_stats():
    if not os.path.exists(LOG_FILE):
        print("⚠️ Log file not found.")
        return

    with open(LOG_FILE, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    if len(rows) <= 1:
        print("⚠️ No entries to analyze.")
        return

    header, entries = rows[0], rows[1:]

    timestamps = [row[0] for row in entries]
    texts = [row[1] for row in entries]
    tags = [row[2] for row in entries if row[2]]

    total_entries = len(entries)
    first_entry = timestamps[0]
    last_entry = timestamps[-1]

    dates = [ts.split()[0] for ts in timestamps]
    unique_days = set(dates)
    date_counts = Counter(dates)
    most_active = date_counts.most_common(1)[0]

    all_words = " ".join(texts).lower().split()
    filtered_words = [word.strip(",.?!") for word in all_words if len(word) > 2]
    word_freq = Counter(filtered_words).most_common(5)
    tag_freq = Counter(tags).most_common(3)

    print("\n📊 careLog Stats")
    print("────────────────────────────")
    print(f"🧾 Total entries     : {total_entries}")
    print(f"📅 First entry date  : {first_entry}")
    print(f"📅 Last entry date   : {last_entry}")
    print(f"📆 Unique days logged: {len(unique_days)}")
    print(f"🔥 Most active day   : {most_active[0]} ({most_active[1]} entries)")
    print("\n🧠 Most common words:")
    for word, count in word_freq:
        print(f"   - {word} ({count} times)")
    print("\n🏷️ Top tags:")
    for tag, count in tag_freq:
        print(f"   - {tag} ({count} times)")

def main():
    init_log_file()

    parser = argparse.ArgumentParser(description="🩺 careLog — CLI health journaling tool")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    parser_log = subparsers.add_parser('log', help='Add a health entry')
    parser_log.add_argument('text', help='Text of the entry (in quotes)')
    parser_log.add_argument('--tag', help='Optional tag for the entry')

    subparsers.add_parser('view', help='View all logged entries')

    parser_filter = subparsers.add_parser('filter', help='Search entries by keyword or tag')
    parser_filter.add_argument('--text', help='Keyword to search for')
    parser_filter.add_argument('--tag', help='Filter by tag')

    parser_delete = subparsers.add_parser('delete', help='Search and delete a log entry by keyword')
    parser_delete.add_argument('keyword', help='Keyword to filter and choose entry to delete')

    parser_edit = subparsers.add_parser('edit', help='Search and edit a log entry by keyword')
    parser_edit.add_argument('keyword', help='Keyword to search for the entry to edit')

    parser_export = subparsers.add_parser('export', help='Export logs to a file')
    parser_export.add_argument('format', choices=['txt', 'json'], help='Export format (txt or json)')

    subparsers.add_parser('stats', help='Show log statistics')

    args = parser.parse_args()

    if args.command == 'log':
        log_entry(args.text, args.tag)
    elif args.command == 'view':
        view_logs()
    elif args.command == 'filter':
        filter_logs(args.text, args.tag)
    elif args.command == 'delete':
        delete_by_keyword(args.keyword)
    elif args.command == 'edit':
        edit_entry(args.keyword)
    elif args.command == 'export':
        export_logs(args.format)
    elif args.command == 'stats':
        show_stats()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
