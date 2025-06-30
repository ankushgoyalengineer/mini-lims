import sqlite3
from datetime import datetime

def create_usage_table():
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sample_reagent_usage (
            usage_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sample_id TEXT NOT NULL,
            reagent_id INTEGER NOT NULL,
            volume_used REAL NOT NULL,
            used_on TEXT,
            used_by TEXT,
            FOREIGN KEY (sample_id) REFERENCES samples(sample_id),
            FOREIGN KEY (reagent_id) REFERENCES reagents(reagent_id)
        );
    """)
    conn.commit()
    conn.close()

def log_sample_reagent_usage():
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()

    # Select sample
    sample_id = input("Enter Sample ID to log usage for: ").strip()
    cursor.execute("SELECT * FROM samples WHERE sample_id = ?", (sample_id,))
    sample = cursor.fetchone()

    if not sample:
        print("❌ Sample ID not found.")
        conn.close()
        return

    if sample[6] == 1:  # Already processed
        print("⚠️ Sample is already marked as processed.")

    # Select reagent
    try:
        reagent_id = int(input("Enter Reagent ID to use: ").strip())
    except ValueError:
        print("❌ Invalid Reagent ID.")
        conn.close()
        return

    cursor.execute("SELECT reagent_name, remaining_volume_ml FROM reagents WHERE reagent_id = ?", (reagent_id,))
    reagent = cursor.fetchone()

    if not reagent:
        print("❌ Reagent not found.")
        conn.close()
        return

    reagent_name, available_volume = reagent

    try:
        volume_used = float(input(f"How much of '{reagent_name}' was used? (Available: {available_volume}): "))
        if volume_used <= 0:
            raise ValueError
    except ValueError:
        print("❌ Invalid volume.")
        conn.close()
        return

    if volume_used > available_volume:
        print("❌ Not enough reagent available.")
        conn.close()
        return

    used_by = input("Who processed this sample? ").strip().title()
    used_on = input("Date of processing (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(used_on, "%Y-%m-%d")
    except ValueError:
        print("❌ Invalid date format.")
        conn.close()
        return

    # Deduct reagent volume
    new_volume = available_volume - volume_used
    cursor.execute("UPDATE reagents SET remaining_volume_ml = ? WHERE reagent_id = ?", (new_volume, reagent_id))

    # Log usage
    cursor.execute("""
        INSERT INTO sample_reagent_usage (sample_id, reagent_id, volume_used, used_on, used_by)
        VALUES (?, ?, ?, ?, ?)
    """, (sample_id, reagent_id, volume_used, used_on, used_by))

    # Mark sample as processed
    cursor.execute("""
        UPDATE samples
        SET is_processed = 1, processed_by = ?, processed_date = ?
        WHERE sample_id = ?
    """, (used_by, used_on, sample_id))

    conn.commit()
    conn.close()
    print(f"✅ Logged {volume_used} units of '{reagent_name}' for Sample ID '{sample_id}'.")

