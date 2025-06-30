from sample_tracker import create_sample_table, add_sample, view_samples
from reagent_tracker import create_reagent_table, register_reagent, update_reagent_stock, view_reagents_by_catalog
from sample_reagent_usage import create_usage_table, log_sample_reagent_usage
from qc_logger import create_qc_table, log_qc_entry, view_qc_logs
from report_generator import generate_sample_report, generate_reagent_report, export_table_to_csv

# Initialize all tables
create_sample_table()
create_reagent_table()
create_usage_table()
create_qc_table()

while True:
    print("\n📋 Mini-LIMS Main Menu:")
    print("1. Register new sample")
    print("2. View existing samples")
    print("3. Register new reagent")
    print("4. Update existing reagent stock")
    print("5. View reagents by catalog number")
    print("6. Log sample-reagent usage")
    print("7. Log quality control entry")
    print("8. View QC logs")
    print("9. Generate sample report")
    print("10. Generate reagent report")
    print("11. Export table to CSV")
    print("12. Exit")

    choice = input("Select an option (1-12): ")

    if choice == '1':
        add_sample()
    elif choice == '2':
        view_samples()
    elif choice == '3':
        register_reagent()
    elif choice == '4':
        update_reagent_stock()
    elif choice == '5':
        view_reagents_by_catalog()
    elif choice == '6':
        log_sample_reagent_usage()
    elif choice == '7':
        log_qc_entry()
    elif choice == '8':
        view_qc_logs()
    elif choice == '9':
        generate_sample_report()
    elif choice == '10':
        generate_reagent_report()
    elif choice == '11':
        table_name = input("Enter the table name to export (e.g., samples, reagents, sample_reagent_usage, quality_control_log): ").strip()
        export_table_to_csv(table_name)
    elif choice == '12':
        print("👋 Goodbye!")
        break
    else:
        print("❌ Invalid choice. Try again.")
