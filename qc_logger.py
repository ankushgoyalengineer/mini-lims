import sqlite3
from datetime import datetime

def create_qc_table():
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quality_control_log (
            qc_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sample_id TEXT,
            reagent_id INTEGER,
            qc_type TEXT NOT NULL,
            qc_result TEXT NOT NULL,
            performed_by TEXT,
            performed_date TEXT,
            remarks TEXT,
            FOREIGN KEY (sample_id) REFERENCES samples(sample_id),
            FOREIGN KEY (reagent_id) REFERENCES reagents(reagent_id)
        );
    """)
    conn.commit()
    conn.close()

def log_qc_entry():
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()

    print("📋 Log Quality Control (QC) Entry")
    sample_id = input("Sample ID (leave blank if N/A): ").strip()
    reagent_id_input = input("Reagent ID (leave blank if N/A): ").strip()
    reagent_id = int(reagent_id_input) if reagent_id_input else None

    if not sample_id and not reagent_id:
        print("❌ You must provide at least a Sample ID or a Reagent ID.")
        conn.close()
        return

    qc_type = input("Type of QC performed (e.g. Mycoplasma Test, pH Check): ").strip()
    qc_result = input("Result (e.g. Pass, Fail, Borderline): ").strip().title()
    performed_by = input("Performed by: ").strip().title()
    performed_date = input("Date of QC (YYYY-MM-DD): ").strip()

    try:
        datetime.strptime(performed_date, "%Y-%m-%d")
    except ValueError:
        print("❌ Invalid date format.")
        conn.close()
        return

    remarks = input("Additional remarks (optional): ").strip()

    cursor.execute("""
        INSERT INTO quality_control_log (
            sample_id, reagent_id, qc_type, qc_result,
            performed_by, performed_date, remarks
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        sample_id if sample_id else None,
        reagent_id,
        qc_type,
        qc_result,
        performed_by,
        performed_date,
        remarks
    ))

    conn.commit()
    conn.close()
    print("✅ QC entry logged successfully.")

def view_qc_logs():
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()

    print("📖 View QC Logs")
    filter_type = input("Filter by (sample/reagent/none): ").strip().lower()

    if filter_type == 'sample':
        sample_id = input("Enter Sample ID to filter: ").strip()
        cursor.execute("SELECT * FROM quality_control_log WHERE sample_id = ?", (sample_id,))
    elif filter_type == 'reagent':
        try:
            reagent_id = int(input("Enter Reagent ID to filter: ").strip())
            cursor.execute("SELECT * FROM quality_control_log WHERE reagent_id = ?", (reagent_id,))
        except ValueError:
            print("❌ Invalid Reagent ID.")
            conn.close()
            return
    else:
        cursor.execute("SELECT * FROM quality_control_log")

    rows = cursor.fetchall()

    if not rows:
        print("📭 No QC logs found.")
    else:
        print(f"{len(rows)} QC Log(s) Found:")
        print("-" * 100)
        for row in rows:
            print(
                f"QC ID: {row[0]} | Sample: {row[1] or 'N/A'} | Reagent: {row[2] or 'N/A'} | "
                f"Type: {row[3]} | Result: {row[4]} | By: {row[5]} | Date: {row[6]} | Remarks: {row[7]}"
            )

    conn.close()
