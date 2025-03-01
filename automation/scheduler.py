import schedule
import time
from data_collection.scraper import collect_patch_data
from data_correlation.correlate import correlate_patch_data
from graph_db.graph_builder import get_db, create_collections, insert_patch_node

def update_patch_intelligence():
    """
    Runs the full update:
    1. Collect patch data from various libraries.
    2. Correlate/enrich the data.
    3. Update the knowledge graph.
    """
    print("Starting update of Patch Intelligence Data...")
    
    # Example: Collect data from multiple sources.
    libraries = [
        ("npm", "express"),
        ("maven", "org.apache:commons-lang3"),
        ("pypi", "requests"),
        ("linux", "5.15.0"),  # kernel version
        ("nuget", "Newtonsoft.Json")
    ]
    
    db = get_db()
    create_collections(db)
    
    for lib, identifier in libraries:
        print(f"\nProcessing {lib} package: {identifier}")
        raw_data = collect_patch_data(lib, identifier)
        if not raw_data:
            print(f"Failed to collect data for {identifier} on {lib}.")
            continue
        enriched_data = correlate_patch_data(raw_data)
        result = insert_patch_node(db, enriched_data)
        print(f"Updated graph for {identifier}: {result}")
    
    print("Update complete.")

def run_scheduler():
    # Schedule the update every hour (or adjust as needed)
    schedule.every(1).hours.do(update_patch_intelligence)
    
    print("Scheduler started. Press Ctrl+C to exit.")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_scheduler()
