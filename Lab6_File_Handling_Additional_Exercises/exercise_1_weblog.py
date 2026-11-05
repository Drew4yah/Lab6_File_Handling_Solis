"""
Exercise 1: Web Server Access Log Analysis
Student: Solis (TUPM-26-2631)
Seed Digit: 1 | ID Sum: 20
Target Status Class: (SEED_DIGIT % 4) + 2 = 3xx
Records to Process: 1000 + ID_SUM = 1020
"""

import os
import csv
import json
import shutil
from collections import Counter
from pathlib import Path

# --- Student Configuration & Data Generation Rules ---
LAST_NAME = "Solis"
STUDENT_ID = "TUPM-26-2631"
SEED_DIGIT = int(STUDENT_ID[-1])  # 1
ID_SUM = sum(int(d) for d in STUDENT_ID if d.isdigit())  # 20

RECORDS_LIMIT = 1000 + ID_SUM  # 1020
TARGET_CLASS_DIGIT = (SEED_DIGIT % 4) + 2  # 3 -> 3xx
TARGET_STATUS_CLASS = f"{TARGET_CLASS_DIGIT}xx"

# --- Directory Setup ---
BASE_DIR = Path(__file__).resolve().parent
DATASET_CANDIDATES = [
    BASE_DIR / "datasets" / "weblog.csv",
    BASE_DIR.parent / "datasets" / "weblog.csv",
    BASE_DIR.parent.parent / "datasets" / "weblog.csv",
]

DATASET_PATH = None
for p in DATASET_CANDIDATES:
    if p.exists():
        DATASET_PATH = p
        break

if not DATASET_PATH:
    # Fallback to local datasets dir
    DATASET_PATH = BASE_DIR / "datasets" / "weblog.csv"

OUTPUT_DIR = BASE_DIR / "output"
BACKUP_DIR = BASE_DIR / "backup"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

FILTERED_CSV_PATH = OUTPUT_DIR / "weblog_3xx_filtered.csv"
JSON_SUMMARY_PATH = OUTPUT_DIR / "weblog_3xx_summary.json"
BACKUP_JSON_PATH = BACKUP_DIR / "weblog_3xx_summary_backup.json"


def run_exercise_1():
    print("=" * 70)
    print("EXERCISE 1: WEB SERVER ACCESS LOG ANALYSIS")
    print("=" * 70)
    print(f"Student: {LAST_NAME} ({STUDENT_ID})")
    print(f"Seed Digit: {SEED_DIGIT} | ID Sum: {ID_SUM}")
    print(f"Target Status Class: {TARGET_STATUS_CLASS}")
    print(f"Records to Process: {RECORDS_LIMIT}")
    print(f"Dataset Path: {DATASET_PATH}")
    print("-" * 70)

    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset file not found at {DATASET_PATH}")

    records_processed = 0
    records_in_target = 0
    invalid_records = 0
    status_counts = Counter()
    url_counts = Counter()
    selected_records = []

    # 1. Read CSV line by line without loading the entire dataset into memory
    with open(DATASET_PATH, mode="r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if records_processed >= RECORDS_LIMIT:
                break
            records_processed += 1

            # 2. Extract IP address, timestamp, requested URL, and HTTP status code
            ip = (row.get("IP") or "").strip()
            time = (row.get("Time") or "").strip()
            url = (row.get("URL") or "").strip()
            status = (row.get("Staus") or row.get("Status") or "").strip()

            # Handle invalid/missing records
            if not status or not status.isdigit():
                invalid_records += 1
                continue

            # 3. Select records whose HTTP status belongs to the target status class
            if status.startswith(str(TARGET_CLASS_DIGIT)) and len(status) == 3:
                records_in_target += 1
                status_counts[status] += 1
                url_counts[url] += 1
                selected_records.append({
                    "IP": ip,
                    "Time": time,
                    "URL": url,
                    "Status": status
                })

    # 4. Count requests per status code and identify 5 most frequently requested URLs
    top_5_urls = url_counts.most_common(5)

    # 5. Export selected records to a filtered CSV file
    fieldnames = ["IP", "Time", "URL", "Status"]
    with open(FILTERED_CSV_PATH, mode="w", encoding="utf-8", newline="") as csv_out:
        writer = csv.DictWriter(csv_out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(selected_records)

    # 5. Write summary to JSON file
    summary_data = {
        "assessment_data": {
            "student_name": LAST_NAME,
            "student_id": STUDENT_ID,
            "seed_digit": SEED_DIGIT,
            "id_sum": ID_SUM,
            "records_processed": records_processed,
            "target_status_class": TARGET_STATUS_CLASS,
            "records_in_target_class": records_in_target,
            "invalid_or_skipped_records": invalid_records,
            "count_per_status_code": dict(status_counts),
            "five_most_requested_urls": [
                {"rank": i + 1, "url": u, "count": c}
                for i, (u, c) in enumerate(top_5_urls)
            ],
            "filtered_csv_file": str(FILTERED_CSV_PATH.name),
            "json_summary_file": str(JSON_SUMMARY_PATH.name)
        }
    }

    with open(JSON_SUMMARY_PATH, mode="w", encoding="utf-8") as json_out:
        json.dump(summary_data, json_out, indent=4)

    # 6. Create a backup of the JSON file and verify that it exists
    shutil.copy2(JSON_SUMMARY_PATH, BACKUP_JSON_PATH)
    backup_verified = BACKUP_JSON_PATH.exists() and BACKUP_JSON_PATH.stat().st_size > 0
    backup_size = BACKUP_JSON_PATH.stat().st_size if backup_verified else 0

    # Display Assessment Data Table
    print("\nASSESSMENT DATA:")
    print("-" * 70)
    print(f"{'Item':<35} | {'Result'}")
    print("-" * 70)
    print(f"{'Records processed':<35} | {records_processed}")
    print(f"{'Target status class':<35} | {TARGET_STATUS_CLASS}")
    print(f"{'Records in target class':<35} | {records_in_target}")
    status_str = ", ".join(f"{k}: {v}" for k, v in sorted(status_counts.items()))
    print(f"{'Count per status code':<35} | {status_str}")
    print(f"{'Five most requested URLs':<35} |")
    for i, (u, c) in enumerate(top_5_urls, 1):
        print(f"  {i}. {u:<50} ({c} requests)")
    print(f"{'Filtered CSV file':<35} | {FILTERED_CSV_PATH.name} ({len(selected_records)} rows)")
    print(f"{'JSON summary file':<35} | {JSON_SUMMARY_PATH.name}")
    print(f"{'Backup verification':<35} | {'VERIFIED' if backup_verified else 'FAILED'} ({BACKUP_JSON_PATH.name}, {backup_size} bytes)")
    print("-" * 70)
    print("\nFINAL OUTPUT: Exercise 1 completed successfully!\n")

    return summary_data


if __name__ == "__main__":
    run_exercise_1()

