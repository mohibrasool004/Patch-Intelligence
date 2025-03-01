import csv
from data_collection.scraper import collect_patch_data
from data_correlation.correlate import correlate_patch_data
from graph_db.graph_builder import get_db, create_collections, insert_patch_node

def main():
    print("Starting Patch Intelligence Pipeline...")
    
    # Define a list of libraries and package identifiers to process.
    packages = [
        ("npm", "express"),
        ("maven", "org.apache:commons-lang3"),
        ("pypi", "requests"),
        ("linux", "5.15.0"),  # Example kernel version
        ("nuget", "Newtonsoft.Json")
    ]
    
    db = get_db()
    create_collections(db)
    
    csv_file_path = "patch_intelligence_output.csv"
    
    # Open the CSV file for writing
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write header
        writer.writerow(["Vendor", "Product", "Fixed Version", "Reference KB", "Vulnerabilities Fixed", "NVD CPE"])
        
        for lib, identifier in packages:
            print(f"\nProcessing {lib} package: {identifier}")
            raw_data = collect_patch_data(lib, identifier)
            if not raw_data:
                print(f"Failed to collect data for {identifier} on {lib}.")
                continue
            
            print("Raw patch data collected:", raw_data)
            enriched_data = correlate_patch_data(raw_data)
            print("Enriched patch data:", enriched_data)
            
            result = insert_patch_node(db, enriched_data)
            print("Graph database update result:", result)
            
            # Write enriched data to CSV
            writer.writerow([
                enriched_data.get('vendor', 'N/A'),
                enriched_data.get('product', 'N/A'),
                enriched_data.get('fixed_version', 'N/A'),
                enriched_data.get('reference_kb', 'N/A'),
                ", ".join(enriched_data.get('vulnerabilities_fixed', [])),  # Convert list to string
                enriched_data.get('nvd_cpe', 'N/A')
            ])
    
    print(f"\nPatch Intelligence Pipeline complete. Output saved to {csv_file_path}")

if __name__ == "__main__":
    main()
