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

# Argument parser
parser = argparse.ArgumentParser(description="🩺 careLog - CLI health journal")
parser.add_argument('command', help="Command to run (e.g. log)")
parser.add_argument('text', nargs='?', help="Text to log (in quotes)")

args = parser.parse_args()

if args.command == "log":
    if args.text:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, args.text])
        print(f"✅ Entry added: [{timestamp}] {args.text}")
    else:
        print("⚠️ Please provide log text in quotes.")
elif args.command == "view":
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            print("📖 Health Log:")
            for row in reader:
                print(f"[{row[0]}] {row[1]}")
    else:
        print("⚠️ No entries found. Try logging something first.")
else:
    print("❌ Unknown command. Use: log or view")

