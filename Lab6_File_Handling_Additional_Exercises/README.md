# Laboratory 6: File Handling — Additional Exercises

**Course:** Computer Programming 2 (Strictly for TUP ECE Students)  
**Student Name:** Solis  
**Student ID:** `TUPM-26-2631`  
**Seed Digit:** `1` (`int(STUDENT_ID[-1])`)  
**ID Sum:** `20` (`2 + 6 + 2 + 6 + 3 + 1`)  

---

## Dedicated Branch & Directory
- **Git Branch:** `activity6-additional-exercises`
- **Directory:** `Lab6_File_Handling_Additional_Exercises/`
- **Repository:** [https://github.com/Drew4yah/Lab6_File_Handling_Solis](https://github.com/Drew4yah/Lab6_File_Handling_Solis)

All exercises were implemented using **Python's built-in file-handling functions and standard modules only** (without Pandas or NumPy), strictly following all student-specific data generation rules.

---

## 1. Web Server Access Log Analysis

### Mission & Rules
Develop a file-based log analyzer that processes a student-specific number of web requests, identifies one HTTP response class, and archives the findings.
- **Dataset:** `weblog.csv` (Kaggle: `shawon10/web-log-dataset`)
- **Records Processed Rule:** First `1000 + ID_SUM` = `1000 + 20` = **1020** data records.
- **Target Status Class Rule:** `(SEED_DIGIT % 4) + 2` = `(1 % 4) + 2` = **3xx** (Redirection codes: 300–399).
- **Log Fields:** `IP`, `Time`, `URL`, `Staus` (dataset column name).

### Assessment Data
| Item | Result |
| :--- | :--- |
| **Records processed** | `1020` |
| **Target status class** | `3xx` |
| **Records in target class** | `164` |
| **Count per status code** | `302: 143`, `304: 21` |
| **Five most requested URLs** | 1. `GET / HTTP/1.1` (45 requests)<br>2. `POST /process.php HTTP/1.1` (35 requests)<br>3. `GET /contestproblem.php?name=RUET%20OJ%20Server%20Testing%20Contest HTTP/1.1` (34 requests)<br>4. `GET /home.php HTTP/1.1` (9 requests)<br>5. `GET /logout.php HTTP/1.1` (7 requests) |
| **Filtered CSV file** | `output/weblog_3xx_filtered.csv` (164 rows) |
| **JSON summary file** | `output/weblog_3xx_summary.json` |
| **Backup verification** | `VERIFIED` (`backup/weblog_3xx_summary_backup.json`, 1,316 bytes) |

**Final Output:** Exercise 1 completed successfully with verified backup and exact count matching.

---

## 2. Mobile Device Usage Profiling

### Mission & Rules
Develop a file-based profiling program that filters device records using student-specific criteria and exports a verified usage summary.
- **Dataset:** `user_behavior_dataset.csv` (Kaggle: `valakhorasani/mobile-device-usage-and-user-behavior-dataset`)
- **Operating System Rule:** Android if `SEED_DIGIT` is even; iOS if odd &rarr; **iOS** (`SEED_DIGIT = 1` is odd).
- **User Behavior Class Rule:** `(SEED_DIGIT % 5) + 1` = `(1 % 5) + 1` = **Class 2**.
- **Exported Fields:** `User ID`, `Device Model`, `Operating System`, `Battery Drain (mAh/day)`, `Data Usage (MB/day)`.

### Assessment Data
| Item | Result |
| :--- | :--- |
| **Operating system and behavior class** | `iOS, Class 2` |
| **Total records in dataset** | `700` |
| **Records matching operating system** | `146` |
| **Records in target behavior class** | `32` |
| **Average battery drain (mAh/day)** | `872.03 mAh/day` |
| **Average data usage (MB/day)** | `451.34 MB/day` |
| **Count verification** | `VERIFIED (32 exported rows == 32 selected records)` |
| **Exported CSV file** | `output/user_behavior_ios_class2.csv` (32 records) |
| **JSON summary file** | `output/user_behavior_ios_class2_summary.json` |
| **Backup file and size** | `backup/user_behavior_ios_class2_backup.csv` (954 bytes) |

**Final Output:** Exercise 2 completed successfully with 100% count verification and verified backup.

---

## 3. Cybersecurity Incident Report

### Mission & Rules
Develop a file-based incident reporting program that processes records for a student-specific year, summarizes attack types, ranks the five costliest incidents by financial loss, and archives findings.
- **Dataset:** `Global_Cybersecurity_Threats_2015-2024.csv` (Kaggle: `atharvasoundankar/global-cybersecurity-threats-2015-2024`)
- **Target Year Rule:** `2015 + SEED_DIGIT` = `2015 + 1` = **2016**.
- **Loss Field:** `Financial Loss (in Million $)`.
- **Count Field:** `Attack Type`.

### Assessment Data
| Item | Result |
| :--- | :--- |
| **Target year** | `2016` |
| **Total records in dataset** | `3000` |
| **Incidents in target year** | `285` |
| **Count per attack type** | `Phishing: 55`<br>`DDoS: 53`<br>`Man-in-the-Middle: 47`<br>`SQL Injection: 47`<br>`Ransomware: 42`<br>`Malware: 41` |
| **Total financial loss (USD millions)** | `$13,947.26 Million` |
| **Average financial loss (USD millions)** | `$48.94 Million` |
| **Five costliest incidents** | 1. `Phishing` — **$99.98M** — Germany (`Telecommunications`)<br>2. `Ransomware` — **$99.88M** — USA (`Telecommunications`)<br>3. `Malware` — **$99.29M** — Brazil (`IT`)<br>4. `Ransomware` — **$99.19M** — USA (`Healthcare`)<br>5. `Phishing` — **$98.72M** — Australia (`Education`) |
| **Filtered CSV file** | `output/cybersecurity_2016_filtered.csv` (285 records) |
| **JSON summary file** | `output/cybersecurity_2016_top5_costliest.json` |
| **Backup verification** | `VERIFIED` (`backup/cybersecurity_2016_top5_costliest_backup.json`, 3,523 bytes) |
| **Report file** | `output/cybersecurity_2016_incident_report.txt` |

**Final Output:** Exercise 3 completed successfully with ranking, tie-breaking, report generation, and backup verification.

---

## File Structure

```
Lab6_File_Handling_Additional_Exercises/
│
├── Exercise_1_Web_Server_Access_Log_Analysis.ipynb  # Interactive notebook for Exercise 1
├── Exercise_2_Mobile_Device_Usage_Profiling.ipynb   # Interactive notebook for Exercise 2
├── Exercise_3_Cybersecurity_Incident_Report.ipynb   # Interactive notebook for Exercise 3
├── Lab6_Additional_Exercises_All.ipynb               # Master consolidated notebook for all exercises
│
├── exercise_1_weblog.py                              # Standalone Python script for Exercise 1
├── exercise_2_mobile_device.py                       # Standalone Python script for Exercise 2
├── exercise_3_cybersecurity.py                       # Standalone Python script for Exercise 3
│
├── output/                                           # Evaluation-ready output artifacts
│   ├── weblog_3xx_filtered.csv
│   ├── weblog_3xx_summary.json
│   ├── user_behavior_ios_class2.csv
│   ├── user_behavior_ios_class2_summary.json
│   ├── cybersecurity_2016_filtered.csv
│   ├── cybersecurity_2016_top5_costliest.json
│   └── cybersecurity_2016_incident_report.txt
│
├── backup/                                           # Verified backup copies
│   ├── weblog_3xx_summary_backup.json
│   ├── user_behavior_ios_class2_backup.csv
│   └── cybersecurity_2016_top5_costliest_backup.json
│
└── README.md                                         # This documentation file
```
