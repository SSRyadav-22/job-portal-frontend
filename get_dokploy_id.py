import requests
import json

# --- EDIT THESE TWO LINES ---
API_URL = "http://localhost:3000/api/project.all"
api_key = "etXUOOfqlFwCyVeuvWYCVVJZgPopJEpvrPTXSnbmLpWDRuIWlRjBsmDdfnhXAhnt"  # Paste your key from Dokploy
# ----------------------------

def find_all_apps():
    print("Connecting to Dokploy...")
    headers = {
        "accept": "application/json",
        "x-api-key": api_key,
    }

    try:
        req = requests.get(API_URL, headers=headers, timeout=30)
        req.raise_for_status()  # This will raise an error if the request failed
        data = req.json()

        print("\nFound the following applications:")
        found_apps = False

        for project in data or []:
            environments = project.get("environments", [])
            for env in environments:
                applications = env.get("applications", [])
                for app in applications:
                    app_name = app.get("appName")
                    app_id = app.get("applicationId")
                    if app_name:
                        found_apps = True
                        # Print the app name and its ID
                        print(f"  - App Name: '{app_name}', ID: '{app_id}'")

        if not found_apps:
            print("  - No applications found.")

    except requests.exceptions.HTTPError as errh:
        print(f"\nHTTP Error: {errh}")
        print(f"Response: {req.text}")
    except requests.exceptions.ConnectionError as errc:
        print(f"\nConnection Error: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"\nTimeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"\nAn Error Occurred: {err}")
    except json.JSONDecodeError:
        print(f"\nError: Could not decode JSON response. Check if API_URL is correct.")
        print(f"Response: {req.text}")

find_all_apps()
