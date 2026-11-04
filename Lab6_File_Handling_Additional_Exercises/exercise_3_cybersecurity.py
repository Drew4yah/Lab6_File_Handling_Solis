"""
Exercise 3: Cybersecurity Incident Report
Student: Solis (TUPM-26-2631)
Seed Digit: 1 | ID Sum: 20
Target Year: 2015 + SEED_DIGIT = 2016
Loss Field: Financial Loss (in Million $)
Count Field: Attack Type
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

TARGET_YEAR = 2015 + SEED_DIGIT  # 2016
LOSS_FIELD = "Financial Loss (in Million $)"
COUNT_FIELD = "Attack Type"

# --- Directory Setup ---
BASE_DIR = Path(__file__).resolve().parent
DATASET_CANDIDATES = [
    BASE_DIR / "datasets" / "Global_Cybersecurity_Threats_2015-2024.csv",
    BASE_DIR.parent / "datasets" / "Global_Cybersecurity_Threats_2015-2024.csv",
    BASE_DIR.parent.parent / "datasets" / "Global_Cybersecurity_Threats_2015-2024.csv",
]

DATASET_PATH = None
for p in DATASET_CANDIDATES:
    if p.exists():
        DATASET_PATH = p
        break

if not DATASET_PATH:
    DATASET_PATH = BASE_DIR / "datasets" / "Global_Cybersecurity_Threats_2015-2024.csv"

OUTPUT_DIR = BASE_DIR / "output"
BACKUP_DIR = BASE_DIR / "backup"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

FILTERED_CSV_PATH = OUTPUT_DIR / "cybersecurity_2016_filtered.csv"
JSON_TOP5_PATH = OUTPUT_DIR / "cybersecurity_2016_top5_costliest.json"
BACKUP_JSON_PATH = BACKUP_DIR / "cybersecurity_2016_top5_costliest_backup.json"
REPORT_TXT_PATH = OUTPUT_DIR / "cybersecurity_2016_incident_report.txt"


def run_exercise_3():
    print("=" * 70)
    print("EXERCISE 3: CYBERSECURITY INCIDENT REPORT")
    print("=" * 70)
    print(f"Student: {LAST_NAME} ({STUDENT_ID})")
    print(f"Seed Digit: {SEED_DIGIT} | ID Sum: {ID_SUM}")
    print(f"Target Year: {TARGET_YEAR}")
    print(f"Loss Field: {LOSS_FIELD}")
    print(f"Count Field: {COUNT_FIELD}")
    print(f"Dataset Path: {DATASET_PATH}")
    print("-" * 70)

    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset file not found at {DATASET_PATH}")

    total_records = 0
    incidents_target_year = 0
    attack_counts = Counter()
    losses = []
    selected_incidents = []

    # 1. Read CSV and select incidents occurring in target year
    with open(DATASET_PATH, mode="r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        original_order = 0

        for row in reader:
            total_records += 1
            year_val = (row.get("Year") or "").strip()

            if year_val == str(TARGET_YEAR):
                original_order += 1
                incidents_target_year += 1

                # 2. Count incidents belonging to each attack type
                attack_type = (row.get(COUNT_FIELD) or "Unknown").strip()
                attack_counts[attack_type] += 1

                # 3. Calculate total and average financial loss (handle invalid values)
                loss_str = (row.get(LOSS_FIELD) or "").strip()
                try:
                    loss_val = float(loss_str)
                except ValueError:
                    loss_val = 0.0

                losses.append(loss_val)

                # Store incident with order index for stable tie-breaking
                incident_dict = dict(row)
                incident_dict["_orig_order"] = original_order
                incident_dict["_loss_float"] = loss_val
                selected_incidents.append(incident_dict)

    # 3. Calculate total and average financial loss
    total_financial_loss = sum(losses)
    avg_financial_loss = (total_financial_loss / len(losses)) if losses else 0.0

    # 4. Identify five incidents with highest financial losses
    # Descending loss, retain original dataset order when tied
    ranked_incidents = sorted(
        selected_incidents,
        key=lambda x: (-x["_loss_float"], x["_orig_order"])
    )
    top_5_costliest = ranked_incidents[:5]

    # Prepare top 5 records for JSON export (clean internal helper keys)
    clean_top_5 = []
    for rank, inc in enumerate(top_5_costliest, 1):
        item = {k: v for k, v in inc.items() if not k.startswith("_")}
        item["Rank"] = rank
        clean_top_5.append(item)

    # Export top 5 to JSON
    json_export_data = {
        "assessment_data": {
            "student_name": LAST_NAME,
            "student_id": STUDENT_ID,
            "seed_digit": SEED_DIGIT,
            "id_sum": ID_SUM,
            "target_year": TARGET_YEAR,
            "total_records_in_dataset": total_records,
            "incidents_in_target_year": incidents_target_year,
            "count_per_attack_type": dict(attack_counts),
            "total_financial_loss_usd_millions": round(total_financial_loss, 2),
            "average_financial_loss_usd_millions": round(avg_financial_loss, 2),
            "five_costliest_incidents": clean_top_5
        }
    }

    with open(JSON_TOP5_PATH, mode="w", encoding="utf-8") as jf:
        json.dump(json_export_data, jf, indent=4)

    # 5. Export selected incidents to filtered CSV file
    csv_fieldnames = [k for k in fieldnames if not k.startswith("_")]
    with open(FILTERED_CSV_PATH, mode="w", encoding="utf-8", newline="") as cf:
        writer = csv.DictWriter(cf, fieldnames=csv_fieldnames)
        writer.writeheader()
        for inc in selected_incidents:
            row_clean = {k: inc[k] for k in csv_fieldnames}
            writer.writerow(row_clean)

    # 5. Create verified backup of the JSON file
    shutil.copy2(JSON_TOP5_PATH, BACKUP_JSON_PATH)
    backup_verified = BACKUP_JSON_PATH.exists() and BACKUP_JSON_PATH.stat().st_size > 0
    backup_size = BACKUP_JSON_PATH.stat().st_size if backup_verified else 0

    # 6. Generate text report
    report_lines = [
        "=" * 70,
        f"CYBERSECURITY INCIDENT REPORT - FISCAL YEAR {TARGET_YEAR}",
        "=" * 70,
        f"Student: {LAST_NAME} ({STUDENT_ID})",
        f"Seed Digit: {SEED_DIGIT} | ID Sum: {ID_SUM}",
        f"Target Year: {TARGET_YEAR}",
        "-" * 70,
        "1. EXECUTIVE SUMMARY & ASSESSMENT METRICS",
        f"  Total records in dataset:             {total_records}",
        f"  Incidents occurring in {TARGET_YEAR}:            {incidents_target_year}",
        f"  Total Financial Loss:                 ${total_financial_loss:,.2f} Million USD",
        f"  Average Financial Loss per Incident:  ${avg_financial_loss:,.2f} Million USD",
        "-" * 70,
        "2. INCIDENTS BY ATTACK TYPE",
    ]
    for att, count in sorted(attack_counts.items(), key=lambda x: -x[1]):
        pct = (count / incidents_target_year * 100) if incidents_target_year else 0
        report_lines.append(f"  - {att:<22}: {count:>3} incidents ({pct:>5.1f}%)")

    report_lines.extend([
        "-" * 70,
        "3. FIVE COSTLIEST INCIDENTS OF 2016",
    ])
    for item in clean_top_5:
        report_lines.append(
            f"  Rank {item['Rank']}: Loss = ${item['Financial Loss (in Million $)']} Million USD\n"
            f"         Attack Type:     {item['Attack Type']}\n"
            f"         Country:         {item['Country']}\n"
            f"         Target Industry: {item['Target Industry']}\n"
            f"         Affected Users:  {item['Number of Affected Users']}\n"
            f"         Defense Used:    {item['Defense Mechanism Used']}\n"
            f"         Vulnerability:   {item['Security Vulnerability Type']}\n"
        )

    report_lines.extend([
        "-" * 70,
        "4. OUTPUT & ARCHIVE VERIFICATION",
        f"  Filtered CSV File:    {FILTERED_CSV_PATH.name} ({len(selected_incidents)} records)",
        f"  JSON Summary File:    {JSON_TOP5_PATH.name} ({JSON_TOP5_PATH.stat().st_size} bytes)",
        f"  Backup JSON File:     {BACKUP_JSON_PATH.name} ({backup_size} bytes)",
        f"  Backup Verification:  {'VERIFIED' if backup_verified else 'FAILED'}",
        f"  Incident Report File: {REPORT_TXT_PATH.name}",
        "=" * 70,
    ])

    report_text = "\n".join(report_lines)
    with open(REPORT_TXT_PATH, mode="w", encoding="utf-8") as rf:
        rf.write(report_text)

    # Display Assessment Data Table
    print("\nASSESSMENT DATA:")
    print("-" * 70)
    print(f"{'Item':<38} | {'Result'}")
    print("-" * 70)
    print(f"{'Target year':<38} | {TARGET_YEAR}")
    print(f"{'Total records in dataset':<38} | {total_records}")
    print(f"{'Incidents in target year':<38} | {incidents_target_year}")
    attack_summary_str = ", ".join(f"{k}: {v}" for k, v in sorted(attack_counts.items(), key=lambda x: -x[1]))
    print(f"{'Count per attack type':<38} | {attack_summary_str}")
    print(f"{'Total financial loss (USD millions)':<38} | ${total_financial_loss:,.2f} Million")
    print(f"{'Average financial loss (USD millions)':<38} | ${avg_financial_loss:,.2f} Million")
    print(f"{'Five costliest incidents':<38} |")
    for item in clean_top_5:
        print(f"  {item['Rank']}. {item['Attack Type']} - ${item['Financial Loss (in Million $)']}M - {item['Country']} ({item['Target Industry']})")
    print(f"{'Filtered CSV file':<38} | {FILTERED_CSV_PATH.name} ({len(selected_incidents)} records)")
    print(f"{'JSON summary file':<38} | {JSON_TOP5_PATH.name}")
    print(f"{'Backup verification':<38} | {'VERIFIED' if backup_verified else 'FAILED'} ({BACKUP_JSON_PATH.name}, {backup_size} bytes)")
    print(f"{'Report file':<38} | {REPORT_TXT_PATH.name}")
    print("-" * 70)
    print("\nFINAL OUTPUT: Exercise 3 completed successfully!\n")

    return json_export_data


if __name__ == "__main__":
    run_exercise_3()
