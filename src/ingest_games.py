import requests
import os
import pandas as pd
import time
from dotenv import load_dotenv

# SETUP
load_dotenv()
API_KEY = os.getenv("RAWG_API_KEY")
BASE_URL = "https://api.rawg.io/api/games"

# CONFIGURATION
# 40 games/page * 75 pages = 3,000 games per genre
PAGES_TO_FETCH = 75
OUTPUT_FILE = "data/raw/gun_vs_ball.csv"

# The "Big 8" Archetypes
GENRES_TO_FETCH = {
    "shooter": "Gun",         # Action, Reflexes
    "sports": "Ball",         # Competitive, Annual
    "role-playing-games-rpg": "Sword", # Narrative, Prestige
    "strategy": "Brain",      # Complexity, PC
    "indie": "Soul",          # High Variance, Art
    "simulation": "Life",     # Sandbox, No Win State
    "racing": "Speed",        # Technical, Mastery
    "family": "Party"         # Casual, Group Play
}

def fetch_games(genre_slug, category_label, max_pages=PAGES_TO_FETCH):
    """
    Fetches games from API and returns a list of dictionaries.
    """
    all_games = []
    
    print(f"--- Ingesting {category_label} ({genre_slug}) ---")
    
    for page in range(1, max_pages + 1):
        try:
            params = {
                "key": API_KEY,
                "genres": genre_slug,
                "ordering": "-added", # Sort by popularity
                "page_size": 40,      # Max allowed by RAWG
                "page": page
            }
            
            response = requests.get(BASE_URL, params=params)
            
            if response.status_code != 200:
                print(f"Failed to fetch page {page}: {response.status_code}")
                break
                
            data = response.json()
            results = data.get('results', [])
            
            if not results:
                print("No more results found.")
                break
            
            # EXTRACT & TRANSFORM
            for game in results:
                # RAWG returns a list of genre objects, we just want the names
                genre_names = [g['name'] for g in game.get('genres', [])]
                
                all_games.append({
                    "id": game['id'],
                    "name": game['name'],
                    "category": category_label, # Our Custom Label
                    "genre_slug": genre_slug,   # The RAWG slug
                    "all_genres": ", ".join(genre_names), # Keep full list for context
                    "metacritic": game.get('metacritic'),
                    "rating": game.get('rating'),         # User Score (out of 5)
                    "playtime": game.get('playtime'),     # Hours
                    "released": game.get('released'),
                    "ratings_count": game.get('ratings_count')
                })
            
            # Simple progress bar
            print(f"[{category_label}] Page {page}/{max_pages} ({len(results)} games)")
            
            # Rate Limiting (Be polite)
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error on page {page}: {e}")
            break
            
    return all_games

def main():
    if not API_KEY:
        print("Error: RAWG_API_KEY not found in .env file.")
        print("Please create a .env file with RAWG_API_KEY=your_key")
        return

    # 1. Create Data Directory
    os.makedirs("data/raw", exist_ok=True)
    
    full_dataset = []

    # 2. Loop through the "Big 8"
    print(f"Starting ingestion for {len(GENRES_TO_FETCH)} genres...")
    
    for slug, label in GENRES_TO_FETCH.items():
        games = fetch_games(slug, label)
        full_dataset.extend(games)
    
    # 3. Save to CSV
    df = pd.DataFrame(full_dataset)
    
    print(f"\n--- INGESTION COMPLETE ---")
    print(f"Total raw records: {len(df)}")
    
    # Remove duplicates (A game might appear in multiple searches)
    df = df.drop_duplicates(subset=['id'])
    print(f"Total unique games: {len(df)}")
    
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Dataset saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()