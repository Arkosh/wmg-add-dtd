import os
import requests

API_KEY = os.environ.get("WM_API_KEY")
BASE_URL = "https://www.westmarches.games/api/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def get_active_character_ids():
    character_ids = []
    page = 1
    
    while True:
        response = requests.get(f"{BASE_URL}/characters", headers=HEADERS, params={"page": page, "pageSize": 500})
        if response.status_code != 200:
            print(f"Failed to fetch characters: {response.text}")
            break
            
        data = response.json()
        characters = data.get("data", [])
        
        # Filter for active characters
        for char in characters:
            if char.get("status") == "active":  # Adjust status value if your community uses a different label
                character_ids.append(char["id"])
                
        pagination = data.get("pagination", {})
        if page >= pagination.get("totalPages", 1):
            break
        page += 1
        
    return character_ids

def distribute_currency(character_ids):
    if not character_ids:
        print("No active characters found.")
        return

    # Using the Bulk Rewards endpoint
    payload = {
        "characterIds": character_ids,
        "currencies": [
            {
                "currencyId": "cmtgoo823001f04idilhp8dur",  # Replace with your specific currency ID
                "amount": 1
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/rewards", headers=HEADERS, json=payload)
    if response.status_code in (200, 201):
        print(f"Successfully granted currency to {len(character_ids)} characters!")
    else:
        print(f"Failed to distribute rewards: {response.text}")

if __name__ == "__main__":
    active_ids = get_active_character_ids()
    distribute_currency(active_ids)
