import requests
import json

# API configuration
API_KEY = "YOUR-API-KEY-HERE"
BASE_URL = "https://api.congress.gov/v3"
HEADERS = {'X-API-Key': API_KEY}

def fetch_members(chamber):
    """Fetch members from the specified chamber (senate or house)"""
    url = f"{BASE_URL}/member/{chamber}/current"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()['members']
    else:
        raise Exception(f"Failed to fetch {chamber} members: {response.status_code}")

def process_senate_members(members):
    """Process senate members data into required format"""
    senate_list = []
    for member in members:
        senator = {
            'name': f"{member['firstName']} {member['lastName']}",
            'state': member['state'],
            'party': member['party'],
            'website': member.get('websiteUrl', '')
        }
        senate_list.append(senator)
    return senate_list

def process_house_members(members):
    """Process house members data into required format"""
    house_list = []
    for member in members:
        representative = {
            'name': f"{member['firstName']} {member['lastName']}",
            'state': member['state'],
            'party': member['party'],
            'website': member.get('websiteUrl', ''),
            'district': member['district']
        }
        house_list.append(representative)
    return house_list

def main():
    # Fetch and process Senate members
    senate_members = fetch_members('senate')
    senate_list = process_senate_members(senate_members)
    
    # Fetch and process House members
    house_members = fetch_members('house')
    house_list = process_house_members(house_members)
    
    # Save to JSON files
    with open('senate_members.json', 'w') as f:
        json.dump(senate_list, f, indent=2)
    
    with open('house_members.json', 'w') as f:
        json.dump(house_list, f, indent=2)

if __name__ == "__main__":
    main()
