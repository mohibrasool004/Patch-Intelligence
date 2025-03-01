from arango import ArangoClient
import yaml
import os

# Load configuration
config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

def get_db():
    """
    Connect to ArangoDB using credentials from config.
    """
    client = ArangoClient(hosts=f"{config['arangodb']['host']}:{config['arangodb']['port']}")
    sys_db = client.db('_system', username=config['arangodb']['username'], password=config['arangodb']['password'])
    
    db_name = config['arangodb']['db_name']
    if not sys_db.has_database(db_name):
        sys_db.create_database(db_name)
        print(f"Database '{db_name}' created.")
    
    db = client.db(db_name, username=config['arangodb']['username'], password=config['arangodb']['password'])
    return db

def create_collections(db):
    """
    Create necessary vertex and edge collections for the knowledge graph.
    """
    collections = {
        "patches": {"type": "document"},
        "vulnerabilities": {"type": "document"},
        "products": {"type": "document"},
        "edges": {"type": "edge"}
    }
    
    for col, props in collections.items():
        if not db.has_collection(col):
            if props["type"] == "document":
                db.create_collection(col)
            else:
                db.create_collection(col, edge=True)
            print(f"Created collection: {col}")
        else:
            print(f"Collection '{col}' already exists.")

def insert_patch_node(db, patch_data):
    """
    Insert the patch node into the 'patches' collection.
    Also creates product and vulnerability nodes if necessary and builds edges.
    """
    patches = db.collection("patches")
    # Insert patch node; let ArangoDB assign _key if not provided.
    patch_meta = patches.insert(patch_data)
    patch_key = patch_meta["_key"]

    # Insert or get product node.
    product_key = insert_or_get_product(db, patch_data["vendor"], patch_data["product"])
    # Create edge from patch to product.
    create_edge(db, f"patches/{patch_key}", f"products/{product_key}", "belongs_to")

    # For each vulnerability fixed, insert or get vulnerability node and link.
    for vuln in patch_data.get("vulnerabilities_fixed", []):
        vuln_key = insert_or_get_vulnerability(db, vuln)
        create_edge(db, f"patches/{patch_key}", f"vulnerabilities/{vuln_key}", "fixes")
    
    return patch_meta

def insert_or_get_product(db, vendor, product):
    """
    Insert a new product node if it doesn't exist; otherwise return the existing key.
    """
    products = db.collection("products")
    # Use a composite key: vendor_product
    prod_key = f"{vendor.lower()}_{product.lower()}"
    if products.has(prod_key):
        return prod_key
    else:
        product_data = {
            "_key": prod_key,
            "vendor": vendor,
            "product": product,
            "metadata": {}
        }
        products.insert(product_data)
        return prod_key

def insert_or_get_vulnerability(db, vulnerability):
    """
    Insert a vulnerability node if it doesn't exist.
    """
    vulnerabilities = db.collection("vulnerabilities")
    # Use vulnerability identifier as key.
    vuln_key = vulnerability.lower().replace("cve-", "cve_")
    if vulnerabilities.has(vuln_key):
        return vuln_key
    else:
        vuln_data = {
            "_key": vuln_key,
            "vulnerability": vulnerability,
            "details": {}
        }
        vulnerabilities.insert(vuln_data)
        return vuln_key

def create_edge(db, from_id, to_id, relation_type):
    """
    Create an edge between two nodes.
    """
    edges = db.collection("edges")
    edge_doc = {
        "_from": from_id,
        "_to": to_id,
        "relation": relation_type
    }
    return edges.insert(edge_doc)

# For testing purposes:
if __name__ == "__main__":
    db = get_db()
    create_collections(db)
    # Example patch data (simulate an enriched patch)
    sample_patch = {
        "_key": "patch_express_4180",
        "vendor": "npm",
        "product": "express",
        "fixed_version": "4.18.0",
        "reference_kb": "https://www.npmjs.com/package/express",
        "vulnerabilities_fixed": ["CVE-2023-1001"],
        "nvd_cpe": "cpe:2.3:a:npm:express:*:*:*:*:*:*:*:*",
        "performance_issues": "No significant issues",
        "crash_likelihood": "Low",
        "reboot_required": False,
        "eol_info": "Supported",
        "mitigations": ["Restart service if needed"],
        "caveats": ["Monitor for rare edge-case bugs"]
    }
    meta = insert_patch_node(db, sample_patch)
    print("Inserted patch node:", meta)
