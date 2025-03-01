import requests
from bs4 import BeautifulSoup
import yaml
import os

# Load configuration
config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

SCRAPE_TIMEOUT = config.get("scrape_timeout", 10)

def fetch_patch_data(url):
    """
    Fetch HTML content from the given URL.
    """
    try:
        response = requests.get(url, timeout=SCRAPE_TIMEOUT)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def scrape_npm(package_identifier):
    """
    Scrape patch data from npm.
    """
    url = config["data_sources"].get("npm").replace("<PACKAGE_NAME>", package_identifier)
    html_content = fetch_patch_data(url)
    # Dummy parsing: In a full implementation, parse html_content with BeautifulSoup.
    patch_data = {
        "vendor": "npm",
        "product": package_identifier,
        "fixed_version": "unknown",  # In a real scrape, extract the actual version.
        "reference_kb": url,
        "vulnerabilities_fixed": [],
        "nvd_cpe": None,
        "performance_issues": "None reported",
        "crash_likelihood": "Low",
        "reboot_required": False,
        "eol_info": "Not applicable",
        "mitigations": [],
        "caveats": []
    }
    return patch_data

def scrape_maven(package_identifier):
    """
    Scrape patch data from Maven.
    Expects package_identifier in the format 'groupId:artifactId'.
    """
    base_url = config["data_sources"].get("maven")
    try:
        group_id, artifact_id = package_identifier.split(":")
    except ValueError:
        print("Maven package identifier must be in the format 'groupId:artifactId'")
        return None
    url = base_url.replace("<GROUP_ID>", group_id).replace("<ARTIFACT_ID>", artifact_id)
    patch_data = {
        "vendor": "Maven",
        "product": artifact_id,
        "fixed_version": "unknown",
        "reference_kb": url,
        "vulnerabilities_fixed": [],
        "nvd_cpe": None,
        "performance_issues": "None reported",
        "crash_likelihood": "Low",
        "reboot_required": False,
        "eol_info": "Not applicable",
        "mitigations": [],
        "caveats": []
    }
    return patch_data

def scrape_pypi(package_identifier):
    """
    Scrape patch data from PyPi.
    """
    url = config["data_sources"].get("pypi").replace("<PACKAGE_NAME>", package_identifier)
    patch_data = {
        "vendor": "PyPi",
        "product": package_identifier,
        "fixed_version": "unknown",
        "reference_kb": url,
        "vulnerabilities_fixed": [],
        "nvd_cpe": None,
        "performance_issues": "None reported",
        "crash_likelihood": "Low",
        "reboot_required": False,
        "eol_info": "Not applicable",
        "mitigations": [],
        "caveats": []
    }
    return patch_data

def scrape_linux(package_identifier):
    """
    For Linux, the package_identifier might be a kernel version.
    """
    url = config["data_sources"].get("linux")
    patch_data = {
        "vendor": "Linux",
        "product": "Kernel",
        "fixed_version": package_identifier,
        "reference_kb": url,
        "vulnerabilities_fixed": [],
        "nvd_cpe": None,
        "performance_issues": "Potential performance impact reported in some kernel patches",
        "crash_likelihood": "Medium",
        "reboot_required": True,
        "eol_info": "Depends on distribution",
        "mitigations": [],
        "caveats": []
    }
    return patch_data

def scrape_nuget(package_identifier):
    """
    Scrape patch data from NuGet.
    """
    url = config["data_sources"].get("nuget").replace("<PACKAGE_NAME>", package_identifier)
    patch_data = {
        "vendor": "NuGet",
        "product": package_identifier,
        "fixed_version": "unknown",
        "reference_kb": url,
        "vulnerabilities_fixed": [],
        "nvd_cpe": None,
        "performance_issues": "None reported",
        "crash_likelihood": "Low",
        "reboot_required": False,
        "eol_info": "Not applicable",
        "mitigations": [],
        "caveats": []
    }
    return patch_data

def collect_patch_data(library, package_identifier):
    """
    Collect patch data for the given library.
    Supported libraries: npm, maven, pypi, linux, nuget.
    """
    library_lower = library.lower()
    if library_lower == "npm":
        return scrape_npm(package_identifier)
    elif library_lower == "maven":
        return scrape_maven(package_identifier)
    elif library_lower == "pypi":
        return scrape_pypi(package_identifier)
    elif library_lower == "linux":
        return scrape_linux(package_identifier)
    elif library_lower == "nuget":
        return scrape_nuget(package_identifier)
    else:
        print(f"Library {library} not supported.")
        return None

# For testing purposes:
if __name__ == "__main__":
    # Example: test npm
    data = collect_patch_data("npm", "express")
    print("Collected patch data for npm:", data)
