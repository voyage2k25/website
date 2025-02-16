import os
import json
import requests
from jinja2 import Template

# Constants
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "../site/p/")
TEMPLATE_FILE = os.path.join(os.path.dirname(__file__), "template.html")

# Load environment variables
API_URL = os.environ.get("API_URL")
API_PASSWORD = os.environ.get("API_KEY")

# Ensure API credentials are available
if not API_URL or not API_PASSWORD:
    print("❌ ERROR: API_URL or API_PASSWORD not set. Aborting.")
    exit(1)

# Default test data
DEFAULT_JSON = {
    "data": [
        {
            "id": "test1",
            "batch": "B.Tech 3rd",
            "food": "Non Veg",
            "items_rec": "T-SHIRT, TIFFIN",
            "name": "Test Person 1",
            "paid": "1100",
            "payable": "1100",
            "tshirt": "Size : XL",
        },
        {
            "id": "test2",
            "batch": "B.Tech 3rd",
            "food": "Non Veg",
            "items_rec": "None",
            "name": "Test Person 2",
            "paid": "900",
            "payable": "1100",
            "tshirt": "Size : XL",
        },
    ]
}

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Fetch data from API
print("🔄 Fetching data from API...")
try:
    response = requests.post(API_URL, json={"password": API_PASSWORD})
    response.raise_for_status()
    api_data = response.json()  # Expected to have a "data" field

    if "data" not in api_data or not isinstance(api_data["data"], list):
        raise ValueError("Invalid API response format. Missing 'data' field.")

    print("✅ API request successful. Merging test data with API data.")
    data = {"data": api_data["data"] + DEFAULT_JSON["data"]}  # Append test data
except (requests.RequestException, ValueError) as e:
    print(f"❌ API request failed: {e}")
    print("⚠️ Using test data only. Aborting.")
    data = DEFAULT_JSON
    exit(1)

# Load HTML template
try:
    with open(TEMPLATE_FILE, "r") as f:
        template_content = f.read()
    template = Template(template_content)
    print("✅ Template loaded successfully.")
except Exception as e:
    print(f"❌ ERROR: Failed to load template: {e}")
    exit(1)

# Generate HTML files
print("📄 Generating HTML pages...")
for item in data["data"]:
    rendered_html = template.render(data=item)
    file_path = os.path.join(OUTPUT_DIR, f"{item['id']}.html")

    with open(file_path, "w") as f:
        f.write(rendered_html)

    print(f"✅ Generated: {file_path}")

print("🎉 Page generation complete!")
