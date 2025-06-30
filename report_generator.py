import sqlite3
import csv
from datetime import datetime

def generate_sample_report():
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM samples")
    rows = cursor.fetchall()

    if not rows:
        print("📭 No samples found.")
    else:
        print("\n📄 Sample Report:")
        print("-" * 80)
        for row in rows:
            print(f"ID: {row[0]} | Sample ID: {row[1]} | Type: {row[2]} | "
                  f"Date: {row[3]} | Source: {row[4]} | Storage: {row[5]} | "
                  f"Processed: {row[6]} | By: {row[7]} | On: {row[8]}")

    conn.close()

def generate_reagent_report():
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reagents")
    rows = cursor.fetchall()

    if not rows:
        print("📭 No reagents found.")
    else:
        print("\n🧾 Reagent Report:")
        print("-" * 100)
        for row in rows:
            print(f"ID: {row[0]} | Name: {row[1]} | Catalog: {row[2]} | Vendor: {row[3]} | "
                  f"Batch: {row[4]} | Stock: {row[5]} x {row[6]} | Location: {row[8]} | "
                  f"Expiry: {row[9]} | Registered By: {row[11]}")

    conn.close()

def export_table_to_csv(table_name, output_file=None):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        col_names = [description[0] for description in cursor.description]

        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"{table_name}_export_{timestamp}.csv"

        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(col_names)
            writer.writerows(rows)

        print(f"✅ Data from '{table_name}' exported successfully to '{output_file}'")
    except Exception as e:
        print(f"❌ Error exporting data: {e}")
    finally:
        conn.close()
