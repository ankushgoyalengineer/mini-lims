import sqlite3
from datetime import datetime

def check_empty_input(s):
    if s.strip():
        print("string cannot be empty")
    else:
        pass


def create_sample_table():
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()

    # Check if 'samples' table exists
    cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='samples';
                """)
    table_exists = cursor.fetchone()

    if table_exists:
        print("ℹ️ Table 'samples' already exists.")
    else:
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS samples (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sample_id TEXT NOT NULL UNIQUE,
                sample_type TEXT,
                collection_date TEXT,
                source TEXT,
                storage_location TEXT,
                is_processed BOOLEAN DEFAULT 0,
                processed_by TEXT,
                processed_on TEXT,
                is_available BOOLEAN DEFAULT 1
                );
            ''')
        print("✅ Table 'samples' created successfully.")

    conn.commit()
    conn.close()

def add_sample():
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()

    while True:
        sample_id = input("Enter the sample ID: ").capitalize()
        if not sample_id.strip():
            print("Sample ID cannot be empty.")
            continue

        cursor.execute("SELECT 1 FROM samples WHERE sample_id = ?", (sample_id,))
        exists = cursor.fetchone()
        if exists:
            print("❌ That Sample ID already exists. Please enter a unique ID.")
        else:
            break

    sample_type = input("Enter the sample type: ").capitalize()
    
    while True:
        collection_date = input("Enter date (MM/DD/YYYY): ")
        try:
            datetime.strptime(collection_date, "%m/%d/%Y")
            break
        except ValueError:
            print("❌ Invalid date format. Please use MM/DD/YYYY.")

    source = input("Enter the source: ").capitalize()
    storage_location = input("Enter the storage location: ").capitalize()

    processed = input("Has the sample already been processed? (yes/no): ").strip().lower()
    if processed == 'yes':
        is_processed = 1
        is_available = 0
        processed_by = input("Enter the name of person who processed it: ").capitalize()

        while True:
            processed_on = input("Enter Processed Date (MM/DD/YYYY): ")
            try:
                datetime.strptime(processed_on, "%m/%d/%Y")
                break
            except ValueError:
                print("❌ Invalid date format. Please use MM/DD/YYYY.")
    else:
        is_processed = 0
        is_available = 1
        processed_by = None
        processed_on = None

    cursor.execute('''
        INSERT INTO samples (
            sample_id, sample_type, collection_date, source,
            storage_location, is_processed, processed_by, processed_on, is_available
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        sample_id, sample_type, collection_date, source,
        storage_location, is_processed, processed_by, processed_on, is_available
    ))

    conn.commit()
    conn.close()
    print("✅ Sample added successfully to the database.")


def view_samples():
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM samples")
    rows = cursor.fetchall()

    if not rows:
        print("📭 No samples found in the database.")
    else:
        print("\n📋 Sample Records:")
        print("-" * 80)
        for row in rows:
            print(f"ID: {row[0]} | Sample ID: {row[1]} | Type: {row[2]} | Date: {row[3]} | Source: {row[4]} | Storage: {row[5]} | "
                  f"Processed: {'Yes' if row[6] else 'No'} | By: {row[7] or '-'} | On: {row[8] or '-'} | Available: {'Yes' if row[9] else 'No'}")

    conn.close()