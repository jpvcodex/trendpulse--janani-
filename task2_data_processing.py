import pandas as pd
import os
from datetime import datetime


# Adjust the filename to match the one you generated in Task 1
json_file = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

if not os.path.exists(json_file):
    print(f"Error: {json_file} not found! Run Task 1 first.")
else:
    df = pd.read_json(json_file)
    print(f"Loaded {len(df)} stories from {json_file}")

    
    
    # Remove duplicates based on post_id
    df = df.drop_duplicates(subset=['post_id'])
    print(f"After removing duplicates: {len(df)}")

    # Drop rows where critical fields (post_id, title, score) are missing
    df = df.dropna(subset=['post_id', 'title', 'score'])
    print(f"After removing nulls: {len(df)}")

    # Ensure score and num_comments are integers
    df['score'] = df['score'].astype(int)
    df['num_comments'] = df['num_comments'].astype(int)

    # Filter out low-quality stories (score < 5)
    df = df[df['score'] >= 5]
    print(f"After removing low scores (<5): {len(df)}")

    # Strip extra whitespace from the title column
    df['title'] = df['title'].str.strip()

    
    csv_path = "data/trends_clean.csv"
    df.to_csv(csv_path, index=False)

    print(f"\nSaved {len(df)} rows to {csv_path}")

    # Print stories-per-category summary
    print("\nStories per category:")
    print(df['category'].value_counts())


