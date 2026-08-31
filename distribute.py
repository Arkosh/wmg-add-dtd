import os
import requests

API_KEY = os.environ.get("WM_API_KEY")
BASE_URL = "https://www.westmarches.games/api/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Replace with your actual currency ID obtained from GET /currencies
CURRENCY_ID = "cmtgoo823001f04idilhp8dur"

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
        
        for char in characters:
            # Check if character is active
            if char.get("status") == "ACTIVE":
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

    success_count = 0
    
    # Distribute individually to ensure reliability and correct endpoint formatting
    for char_id in character_ids:
        payload = {
            "currencies": {
                CURRENCY_ID: 1
            },
            "reason": "Weekly automated currency distribution"
        }
        
        response = requests.post(f"{BASE_URL}/characters/{char_id}/rewards", headers=HEADERS, json=payload)
        if response.status_code in (200, 201):
            success_count += 1
        else:
            print(f"Failed for character {char_id}: {response.text}")

    print(f"Successfully granted currency to {success_count}/{len(character_ids)} active characters.")

if __name__ == "__main__":
    active_ids = get_active_character_ids()
    distribute_currency(active_ids)
