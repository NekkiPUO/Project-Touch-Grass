import requests
import os
from dotenv import load_dotenv
import pandas as pd

# Load the API Key safely
load_dotenv()
API_KEY = os.getenv("RAWG_API_KEY")
BASE_URL = "https://api.rawg.io/api"

def get_games_by_genre(genre_slug, page_size=5):
    """
    Fetches top games for a specific genre (e.g., 'shooter', 'sports')
    """
    url = f"{BASE_URL}/games"
    params = {
        "key": API_KEY,
        "genres": genre_slug,
        "ordering": "-added", # Sort by popularity (most added to libraries)
        "page_size": page_size
    }
    
    print(f"Fetching {genre_slug} data...")
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return []
    
    data = response.json()
    return data['results']

def main():
    if not API_KEY:
        print("Error: RAWG_API_KEY not found in .env file")
        return

    # 1. Fetch Shooters ("Gun")
    shooters = get_games_by_genre("shooter")
    
    # 2. Fetch Sports ("Ball")
    sports = get_games_by_genre("sports")
    
    # 3. Compare Data Structure
    # We want to see if we have Metacritic scores and Playtime
    print("\n--- DATA CHECK ---")
    
    sample_game = shooters[0]
    print(f"Game: {sample_game['name']}")
    print(f"Metacritic: {sample_game.get('metacritic')}")
    print(f"Avg Playtime: {sample_game.get('playtime')} hours")
    print(f"Rating (User): {sample_game.get('rating')}/5.0")
    print(f"Genres: {[g['name'] for g in sample_game['genres']]}")

if __name__ == "__main__":
    main()