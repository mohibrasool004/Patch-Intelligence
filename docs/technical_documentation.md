# Patch Intelligence Technical Documentation

## Overview
The Patch Intelligence system is designed to:
1. **Collect** patch data from multiple vendors/package libraries.
2. **Correlate** patch data with vulnerability data (CVEs), product identifiers (CPEs), and ITSM intelligence.
3. **Organize** the data into a bidirectional knowledge graph stored in ArangoDB.
4. **Automate** the update process.

## Modules

### Data Collection (`data_collection/scraper.py`)
- Contains dedicated functions for scraping patch data from npm, Maven, PyPi, Linux, and NuGet.
- Uses Python’s `requests` and `BeautifulSoup` libraries.
- Returns an actionable data structure with fields such as vendor, product, fixed version, vulnerabilities fixed, and ITSM intelligence.

### Data Correlation (`data_correlation/correlate.py`)
- Enriches raw patch data with CVE and CPE information.
- Adds additional intelligence from vendor disclosures (performance issues, crash likelihood, reboot requirements, EOL info, mitigations, and caveats).

### Graph Database (`graph_db/graph_builder.py`)
- Connects to ArangoDB using `python-arango` and creates necessary collections:
  - `patches`, `vulnerabilities`, `products`, and `edges`
- Inserts nodes for patches, products, and vulnerabilities.
- Creates relationships (edges) linking patches to products and vulnerabilities.

### Automation (`automation/scheduler.py`)
- Uses the `schedule` library to run periodic updates of the full data collection–correlation–graph update pipeline.

## Running the Project
- Use `main.py` to run the entire pipeline once.
- For periodic updates, run the scheduler:
  ```bash
  python automation/scheduler.py
