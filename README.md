# Patch Intelligence Information System

This project builds a Patch Intelligence Information System that:
- Collects patch data for top package libraries (npm, Maven, PyPi, Linux, NuGet)
- Correlates patch data with vulnerability information (CVEs) and product identifiers (CPEs)
- Organizes the data into a bidirectional knowledge graph stored in ArangoDB
- Automates periodic updates of data collection, correlation, and graph updating

## Directory Structure
- **config/**: Contains configuration files.
- **docs/**: Technical documentation.
- **data_collection/**: Web-scraping code to collect patch data.
- **data_correlation/**: Code to correlate/enrich patch data with vulnerability and ITSM intelligence.
- **graph_db/**: Code to create/update the knowledge graph in ArangoDB.
- **automation/**: Scheduler scripts for periodic updates.
- **main.py**: Orchestrates the complete pipeline.

## Setup Instructions
1. Install Python 3.7+ and [pip](https://pip.pypa.io/en/stable/).
2. Install required packages:
   ```bash
   pip install -r requirements.txt
