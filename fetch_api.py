import urllib.request
import json
import os

url = "https://script.google.com/macros/s/AKfycbw3uiWEmW9Vvyj_iewhuzPfOVe29hK72vKf79N_gVheg4ZKRWEP3u_UQ412pEpcghFi/exec"
key = "Bright2017"

def fetch(action, params=""):
    full_url = f"{url}?key={key}&action={action}{params}"
    print(f"Fetching {action}...")
    try:
        req = urllib.request.Request(
            full_url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            return json.loads(html)
    except Exception as e:
        print(f"Error fetching {action}: {e}")
        # Try following redirect manually if needed, but urllib.request follows redirects by default.
        return None

os.makedirs("api_cache", exist_ok=True)

# 1. Sheets
sheets_res = fetch("sheets")
if not sheets_res:
    print("Could not fetch sheets. Trying to output raw response.")
    # Try a simple fetch and print
    try:
        with urllib.request.urlopen(f"{url}?key={key}&action=sheets") as r:
            print(r.read().decode('utf-8')[:500])
    except Exception as ex:
        print("Raw fetch error:", ex)
    exit(1)

with open("api_cache/sheets.json", "w", encoding="utf-8") as f:
    json.dump(sheets_res, f, indent=2, ensure_ascii=False)

sheets = sheets_res.get("sheets", [])
print(f"Found sheets: {[s['name'] for s in sheets]}")

for sheet in sheets:
    name = sheet["name"]
    # 2. Schema
    schema = fetch("schema", f"&sheet={urllib.parse.quote(name)}")
    if schema:
        with open(f"api_cache/schema_{name}.json", "w", encoding="utf-8") as f:
            json.dump(schema, f, indent=2, ensure_ascii=False)
            
    # 3. Analyze
    analyze = fetch("analyze", f"&sheet={urllib.parse.quote(name)}")
    if analyze:
        with open(f"api_cache/analyze_{name}.json", "w", encoding="utf-8") as f:
            json.dump(analyze, f, indent=2, ensure_ascii=False)
            
    # 4. Data
    data = fetch("data", f"&sheet={urllib.parse.quote(name)}")
    if data:
        with open(f"api_cache/data_{name}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

print("Done caching API data.")
