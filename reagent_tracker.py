import sqlite3
from datetime import datetime

def create_reagent_table():
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reagents (
            reagent_id INTEGER PRIMARY KEY AUTOINCREMENT,
            reagent_name TEXT NOT NULL,
            catalog_number TEXT NOT NULL,
            vendor TEXT,
            batch_number TEXT,
            unit_count INTEGER NOT NULL,
            unit_description TEXT NOT NULL,
            volume_per_unit REAL,
            unit TEXT,
            remaining_volume_ml REAL,
            lab TEXT,
            storage_location TEXT,
            expiry_date TEXT,
            arrival_date TEXT,
            registered_by TEXT,
            notes TEXT
        );
    """)
    conn.commit()
    conn.close()

def register_reagent():
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()

    def get_input(prompt, required=True, validate=None, transform=None):
        while True:
            value = input(prompt).strip()
            if not value and required:
                print("This field is required.")
                continue
            if validate and value:
                try:
                    if not validate(value):
                        raise ValueError
                except:
                    print("Invalid format. Please try again.")
                    continue
            return transform(value) if transform and value else value

    def validate_date(date_str):
        datetime.strptime(date_str, "%Y-%m-%d")
        return True

    def validate_int(n):
        return int(n) > 0

    def validate_float(n):
        return float(n) > 0

    reagent_name = get_input("Reagent Name: ", transform=str.title)
    catalog_number = get_input("Catalog Number: ")
    vendor = get_input("Vendor (optional): ", required=False)
    batch_number = get_input("Batch Number (optional): ", required=False)
    unit_count = get_input("How many containers/units received? ", validate=validate_int, transform=int)
    unit_description = get_input("Describe container (e.g., 500 mL bottle): ")
    volume_per_unit = get_input("Volume per unit (e.g., 500): ", validate=validate_float, transform=float)
    unit = get_input("Unit (e.g., mL, g): ")
    lab = get_input("Lab (optional): ", required=False)
    storage_location = get_input("Storage Location: ")
    expiry_date = get_input("Expiry Date (YYYY-MM-DD, optional): ", required=False, validate=validate_date)
    arrival_date = get_input("Arrival Date (YYYY-MM-DD, optional): ", required=False, validate=validate_date)
    registered_by = get_input("Registered By: ", transform=str.title)
    notes = get_input("Notes (optional): ", required=False)

    remaining_volume_ml = unit_count * volume_per_unit

    cursor.execute("""
        INSERT INTO reagents (
            reagent_name, catalog_number, vendor, batch_number,
            unit_count, unit_description, volume_per_unit, unit, remaining_volume_ml,
            lab, storage_location, expiry_date, arrival_date, registered_by, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        reagent_name, catalog_number, vendor, batch_number,
        unit_count, unit_description, volume_per_unit, unit, remaining_volume_ml,
        lab, storage_location, expiry_date, arrival_date, registered_by, notes
    ))

    conn.commit()
    conn.close()
    print(f"✅ Reagent '{reagent_name}' registered successfully.")

def update_reagent_stock():
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()

    catalog_number = input("Enter the catalog number of the reagent to update: ").strip()
    cursor.execute("""
        SELECT reagent_id, reagent_name, vendor, batch_number, unit_count, volume_per_unit, unit
        FROM reagents
        WHERE catalog_number = ?
    """, (catalog_number,))
    matches = cursor.fetchall()

    if not matches:
        print("❌ No reagents found with that catalog number.")
        conn.close()
        return

    print("\nMatching reagents:")
    for row in matches:
        print(f"ID: {row[0]}, Name: {row[1]}, Vendor: {row[2]}, Batch: {row[3]}, Unit Count: {row[4]} x {row[5]} {row[6]}")

    try:
        selected_id = int(input("Enter the ID of the reagent to update: ").strip())
    except ValueError:
        print("❌ Invalid ID.")
        conn.close()
        return

    cursor.execute("SELECT unit_count, volume_per_unit FROM reagents WHERE reagent_id = ?", (selected_id,))
    result = cursor.fetchone()
    if not result:
        print("❌ Reagent ID not found.")
        conn.close()
        return

    current_units, volume_per_unit = result
    try:
        change = int(input(f"Current unit count is {current_units}. Enter quantity to add (use negative for reduction): "))
    except ValueError:
        print("❌ Invalid quantity.")
        conn.close()
        return

    new_units = current_units + change
    if new_units < 0:
        print("❌ Resulting stock cannot be negative.")
        conn.close()
        return

    new_volume = new_units * volume_per_unit
    cursor.execute("UPDATE reagents SET unit_count = ?, remaining_volume_ml = ? WHERE reagent_id = ?", 
                   (new_units, new_volume, selected_id))
    conn.commit()
    conn.close()
    print(f"✅ Stock updated. New unit count: {new_units}, New volume: {new_volume}.")

def view_reagents_by_catalog():
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()

    catalog_number = input("Enter catalog number to search for: ").strip()
    cursor.execute("""
        SELECT reagent_id, reagent_name, vendor, batch_number, unit_count,
               unit_description, volume_per_unit, unit, remaining_volume_ml, lab,
               storage_location, expiry_date, arrival_date, registered_by, notes
        FROM reagents
        WHERE catalog_number = ?
    """, (catalog_number,))

    rows = cursor.fetchall()

    if not rows:
        print("📭 No reagents found with that catalog number.")
    else:
        print(f"\n🔍 Reagents matching catalog number '{catalog_number}':")
        print("-" * 100)
        for row in rows:
            print(
                f"ID: {row[0]} | Name: {row[1]} | Vendor: {row[2]} | Batch: {row[3]} | "
                f"Stock: {row[4]} x {row[5]} | Volume: {row[6]} {row[7]} | Remaining: {row[8]} {row[7]} | "
                f"Lab: {row[9]} | Location: {row[10]} | Expiry: {row[11]} | Arrival: {row[12]} | "
                f"Registered By: {row[13]} | Notes: {row[14]}"
            )

    conn.close()
