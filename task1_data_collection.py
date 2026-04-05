import requests
import json
import time
import os
from datetime import datetime

# Configuration and Constants
BASE_URL = "https://hacker-news.firebaseio.com/v0"
HEADERS = {"User-Agent": "TrendPulse/1.0"}
CATEGORY_LIMIT = 25
DATA_DIR = "data"

# Keyword mapping for categorization
CATEGORY_MAP = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}

def fetch_top_stories():
    """Step 1: Fetch the first 500 top story IDs."""
    try:
        response = requests.get(f"{BASE_URL}/topstories.json", headers=HEADERS)
        response.raise_for_status()
        return response.json()[:500]
    except Exception as e:
        print(f"Error fetching top stories: {e}")
        return []

def get_story_details(story_id):
    """Step 2: Fetch individual story details."""
    try:
        response = requests.get(f"{BASE_URL}/item/{story_id}.json", headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception:
        # If a request fails, we print and move on as per instructions
        print(f"Failed to fetch story ID: {story_id}")
        return None

def categorize_title(title):
    """Assign a category based on keywords in the title."""
    title_lower = title.lower()
    for category, keywords in CATEGORY_MAP.items():
        for word in keywords:
            if word.lower() in title_lower:
                return category
    return None

def main():
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    print("Fetching top stories from HackerNews...")
    story_ids = fetch_top_stories()
    
    all_collected_stories = []
    # Track which IDs we've already processed to avoid redundant API calls
    # across different category loops
    processed_cache = {} 
    
    # We iterate by category to follow the requirement: "Wait 2 seconds between each category"
    for category_name in CATEGORY_MAP.keys():
        print(f"Processing category: {category_name}...")
        category_count = 0
        
        for s_id in story_ids:
            if category_count >= CATEGORY_LIMIT:
                break
                
            # Check if we already fetched this item in a previous category loop
            story = processed_cache.get(s_id)
            if story is None:
                story = get_story_details(s_id)
                if story:
                    processed_cache[s_id] = story
            
            if story and "title" in story:
                # Check if this specific story fits the current category loop
                if categorize_title(story["title"]) == category_name:
                    story_data = {
                        "post_id": story.get("id"),
                        "title": story.get("title"),
                        "category": category_name,
                        "score": story.get("score", 0),
                        "num_comments": story.get("descendants", 0),
                        "author": story.get("by"),
                        "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    all_collected_stories.append(story_data)
                    category_count += 1
        
        # Wait 2 seconds between each category loop as required
        time.sleep(2)

    # Save to JSON
    date_str = datetime.now().strftime("%Y%m%d")
    file_path = os.path.join(DATA_DIR, f"trends_{date_str}.json")
    
    with open(file_path, "w") as f:
        json.dump(all_collected_stories, f, indent=4)
    
    print(f"Collected {len(all_collected_stories)} stories. Saved to {file_path}")

if __name__ == "__main__":
    main()
