import os
import requests

API_KEY = os.environ.get("WM_API_KEY")
BASE_URL = "https://www.westmarches.games/api/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Replace with your actual currency ID obtained from GET /currencies
CURRENCY_ID = "cmsxap1iv000104k3uzlhl5i1"
AMOUNT_TO_GIVE = 1

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
            if char.get("status") == "ACTIVE":
                character_ids.append(char["id"])
                
        pagination = data.get("pagination", {})
        if page >= pagination.get("totalPages", 1):
            break
        page += 1
        
    return character_ids

def distribute_bulk_currency(character_ids):
    if not character_ids:
        print("No active characters found.")
        return

    # Build the rewards array required by POST /rewards (bulk)
    rewards_list = []
    for char_id in character_ids:
        rewards_list.append({
            "characterId": char_id,
            "currencies": {
                CURRENCY_ID: AMOUNT_TO_GIVE
            },
            "reason": "Arkozh trying something behind the scene please ignore"
        })

    payload = {
        "rewards": rewards_list
    }
    
    response = requests.post(f"{BASE_URL}/rewards", headers=HEADERS, json=payload)
    if response.status_code in (200, 201):
        print(f"Successfully granted currency to {len(character_ids)} active characters via bulk request!")
    else:
        print(f"Failed to distribute bulk rewards: {response.text}")

if __name__ == "__main__":
    active_ids = get_active_character_ids()
    distribute_bulk_currency(active_ids)
