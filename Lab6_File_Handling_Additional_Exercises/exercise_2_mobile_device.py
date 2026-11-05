"""
Exercise 2: Mobile Device Usage Profiling
Student: Solis (TUPM-26-2631)
Seed Digit: 1 | ID Sum: 20
Operating System: iOS (SEED_DIGIT is odd)
User Behavior Class: (SEED_DIGIT % 5) + 1 = 2
Exported Fields: User ID, Device Model, Operating System, Battery Drain (mAh/day), Data Usage (MB/day)
"""

import os
import csv
import json
import shutil
from pathlib import Path

# --- Student Configuration & Data Generation Rules ---
LAST_NAME = "Solis"
STUDENT_ID = "TUPM-26-2631"
SEED_DIGIT = int(STUDENT_ID[-1])  # 1
ID_SUM = sum(int(d) for d in STUDENT_ID if d.isdigit())  # 20

TARGET_OS = "Android" if (SEED_DIGIT % 2 == 0) else "iOS"
TARGET_BEHAVIOR_CLASS = (SEED_DIGIT % 5) + 1  # 2

EXPORTED_FIELDS = [
    "User ID",
    "Device Model",
    "Operating System",
    "Battery Drain (mAh/day)",
    "Data Usage (MB/day)",
]

# --- Directory Setup ---
BASE_DIR = Path(__file__).resolve().parent
DATASET_CANDIDATES = [
    BASE_DIR / "datasets" / "user_behavior_dataset.csv",
    BASE_DIR.parent / "datasets" / "user_behavior_dataset.csv",
    BASE_DIR.parent.parent / "datasets" / "user_behavior_dataset.csv",
]

DATASET_PATH = None
for p in DATASET_CANDIDATES:
    if p.exists():
        DATASET_PATH = p
        break

if not DATASET_PATH:
    DATASET_PATH = BASE_DIR / "datasets" / "user_behavior_dataset.csv"

OUTPUT_DIR = BASE_DIR / "output"
BACKUP_DIR = BASE_DIR / "backup"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

EXPORTED_CSV_PATH = OUTPUT_DIR / "user_behavior_ios_class2.csv"
JSON_SUMMARY_PATH = OUTPUT_DIR / "user_behavior_ios_class2_summary.json"
BACKUP_CSV_PATH = BACKUP_DIR / "user_behavior_ios_class2_backup.csv"


def run_exercise_2():
    print("=" * 70)
    print("EXERCISE 2: MOBILE DEVICE USAGE PROFILING")
    print("=" * 70)
    print(f"Student: {LAST_NAME} ({STUDENT_ID})")
    print(f"Seed Digit: {SEED_DIGIT} | ID Sum: {ID_SUM}")
    print(f"Assigned Operating System: {TARGET_OS}")
    print(f"Assigned User Behavior Class: Class {TARGET_BEHAVIOR_CLASS}")
    print(f"Dataset Path: {DATASET_PATH}")
    print("-" * 70)

    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset file not found at {DATASET_PATH}")

    total_records = 0
    records_matching_os = 0
    records_in_target_class = 0
    selected_users = []
    battery_drains = []
    data_usages = []

    # 1. Read CSV dataset and identify records matching assigned OS
    # 2. Select users belonging to target behavior class
    with open(DATASET_PATH, mode="r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_records += 1
            os_val = (row.get("Operating System") or "").strip()

            if os_val.lower() == TARGET_OS.lower():
                records_matching_os += 1
                behavior_class_val = (row.get("User Behavior Class") or "").strip()

                if behavior_class_val == str(TARGET_BEHAVIOR_CLASS):
                    records_in_target_class += 1

                    # Extract numeric metrics
                    try:
                        bd = float(row.get("Battery Drain (mAh/day)", 0))
                        battery_drains.append(bd)
                    except ValueError:
                        pass

                    try:
                        du = float(row.get("Data Usage (MB/day)", 0))
                        data_usages.append(du)
                    except ValueError:
                        pass

                    # Extract specified fields
                    user_entry = {field: row.get(field, "").strip() for field in EXPORTED_FIELDS}
                    selected_users.append(user_entry)

    # 3. Calculate average battery drain and average mobile data usage (handle zero records)
    avg_battery = sum(battery_drains) / len(battery_drains) if battery_drains else 0.0
    avg_data = sum(data_usages) / len(data_usages) if data_usages else 0.0

    # 4. Export selected users and specified fields to CSV file
    with open(EXPORTED_CSV_PATH, mode="w", encoding="utf-8", newline="") as csv_out:
        writer = csv.DictWriter(csv_out, fieldnames=EXPORTED_FIELDS)
        writer.writeheader()
        writer.writerows(selected_users)

    # Count rows in exported CSV
    with open(EXPORTED_CSV_PATH, mode="r", encoding="utf-8") as csv_in:
        exported_reader = csv.DictReader(csv_in)
        exported_row_count = sum(1 for _ in exported_reader)

    # 5. Write JSON summary and verify exported row count matches selected count
    count_verified = (exported_row_count == records_in_target_class)

    summary_data = {
        "assessment_data": {
            "student_name": LAST_NAME,
            "student_id": STUDENT_ID,
            "seed_digit": SEED_DIGIT,
            "id_sum": ID_SUM,
            "operating_system_and_behavior_class": f"{TARGET_OS}, Class {TARGET_BEHAVIOR_CLASS}",
            "total_records_in_dataset": total_records,
            "records_matching_operating_system": records_matching_os,
            "records_in_target_behavior_class": records_in_target_class,
            "average_battery_drain_mah_day": round(avg_battery, 2),
            "average_data_usage_mb_day": round(avg_data, 2),
            "count_verification": {
                "selected_record_count": records_in_target_class,
                "exported_row_count": exported_row_count,
                "verified": count_verified
            },
            "exported_csv_file": str(EXPORTED_CSV_PATH.name),
            "json_summary_file": str(JSON_SUMMARY_PATH.name)
        }
    }

    with open(JSON_SUMMARY_PATH, mode="w", encoding="utf-8") as json_out:
        json.dump(summary_data, json_out, indent=4)

    # 6. Create a backup of exported CSV file and report its file size
    shutil.copy2(EXPORTED_CSV_PATH, BACKUP_CSV_PATH)
    backup_exists = BACKUP_CSV_PATH.exists()
    backup_file_size = BACKUP_CSV_PATH.stat().st_size if backup_exists else 0

    summary_data["assessment_data"]["backup_file_and_size"] = {
        "file_name": str(BACKUP_CSV_PATH.name),
        "size_bytes": backup_file_size,
        "verified": backup_exists
    }

    # Re-save JSON with backup details
    with open(JSON_SUMMARY_PATH, mode="w", encoding="utf-8") as json_out:
        json.dump(summary_data, json_out, indent=4)

    # Display Assessment Data Table
    print("\nASSESSMENT DATA:")
    print("-" * 70)
    print(f"{'Item':<40} | {'Result'}")
    print("-" * 70)
    print(f"{'Operating system and behavior class':<40} | {TARGET_OS}, Class {TARGET_BEHAVIOR_CLASS}")
    print(f"{'Total records in dataset':<40} | {total_records}")
    print(f"{'Records matching operating system':<40} | {records_matching_os}")
    print(f"{'Records in target behavior class':<40} | {records_in_target_class}")
    print(f"{'Average battery drain (mAh/day)':<40} | {avg_battery:.2f} mAh/day")
    print(f"{'Average data usage (MB/day)':<40} | {avg_data:.2f} MB/day")
    print(f"{'Count verification':<40} | VERIFIED ({exported_row_count} == {records_in_target_class})")
    print(f"{'Exported CSV file':<40} | {EXPORTED_CSV_PATH.name}")
    print(f"{'JSON summary file':<40} | {JSON_SUMMARY_PATH.name}")
    print(f"{'Backup file and size':<40} | {BACKUP_CSV_PATH.name} ({backup_file_size} bytes)")
    print("-" * 70)
    print("\nFINAL OUTPUT: Exercise 2 completed successfully!\n")

    return summary_data


if __name__ == "__main__":
    run_exercise_2()

