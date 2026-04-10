import pandas as pd
import numpy as np
import os

# 1 — Load and Explore (4 marks)
csv_path = "data/trends_clean.csv"

if not os.path.exists(csv_path):
    print(f"Error: {csv_path} not found! Run Task 2 first.")
else:
    df = pd.read_csv(csv_path)
    
    # Print basic info
    print(f"Loaded data: {df.shape}")
    print("\nFirst 5 rows:")
    print(df.head())
    
    avg_score = df['score'].mean()
    avg_comments = df['num_comments'].mean()
    print(f"\nAverage score   : {avg_score:.2f}")
    print(f"Average comments: {avg_comments:.2f}")

    # 2 — Basic Analysis with NumPy (8 marks)
    # Convert columns to numpy arrays for calculation
    scores = df['score'].to_numpy()
    comments = df['num_comments'].to_numpy()

    print("\n--- NumPy Stats ---")
    print(f"Mean score   : {np.mean(scores):.2f}")
    print(f"Median score : {np.median(scores):.2f}")
    print(f"Std deviation: {np.std(scores):.2f}")
    print(f"Max score    : {np.max(scores)}")
    print(f"Min score    : {np.min(scores)}")

    # Category with most stories
    most_popular_cat = df['category'].value_counts().idxmax()
    cat_count = df['category'].value_counts().max()
    print(f"\nMost stories in: {most_popular_cat} ({cat_count} stories)")

    # Story with most comments
    max_comment_idx = np.argmax(comments)
    most_commented_title = df.iloc[max_comment_idx]['title']
    most_commented_count = df.iloc[max_comment_idx]['num_comments']
    print(f"\nMost commented story: \"{most_commented_title}\" — {most_commented_count} comments")

    # 3 — Add New Columns (5 marks)
    # engagement = num_comments / (score + 1)
    df['engagement'] = df['num_comments'] / (df['score'] + 1)
    
    # is_popular = True if score > average score
    df['is_popular'] = df['score'] > avg_score

    # 4 — Save the Result (3 marks)
    output_path = "data/trends_analysed.csv"
    df.to_csv(output_path, index=False)
    
    print(f"\nSaved {len(df)} rows with new columns to {output_path}")
