import pandas as pd
import matplotlib.pyplot as plt
import os

# 1 — Setup (2 marks)
# Load analysed data from Task 3
csv_path = "data/trends_analysed.csv"
if not os.path.exists(csv_path):
    print(f"Error: {csv_path} not found! Run Task 3 first.")
else:
    df = pd.read_csv(csv_path)
    
    # Create outputs/ folder if it doesn't exist
    if not os.path.exists('outputs'):
        os.makedirs('outputs')

    # 2 — Chart 1: Top 10 Stories by Score (6 marks)
    # Get top 10 stories by score
    top_10 = df.nlargest(10, 'score').sort_values('score', ascending=True)
    
    # Shorten titles longer than 50 characters
    y_labels = [t[:47] + '...' if len(t) > 50 else t for t in top_10['title']]

    plt.figure(figsize=(10, 6))
    plt.barh(y_labels, top_10['score'], color='skyblue')
    plt.title('Top 10 Stories by Score')
    plt.xlabel('Upvote Score')
    plt.ylabel('Story Title')
    plt.tight_layout()
    plt.savefig('outputs/chart1_top_stories.png')
    plt.show()

    # 3 — Chart 2: Stories per Category (6 marks)
    cat_counts = df['category'].value_counts()
    colors = plt.cm.get_cmap('viridis', len(cat_counts)) # Different color for each bar

    plt.figure(figsize=(8, 6))
    plt.bar(cat_counts.index, cat_counts.values, color=colors(range(len(cat_counts))))
    plt.title('Stories per Category')
    plt.xlabel('Category')
    plt.ylabel('Number of Stories')
    plt.savefig('outputs/chart2_categories.png')
    plt.show()

    # 4 — Chart 3: Score vs Comments (6 marks)
    plt.figure(figsize=(8, 6))
    
    # Separate popular and non-popular for the legend
    popular = df[df['is_popular'] == True]
    non_popular = df[df['is_popular'] == False]
    
    plt.scatter(popular['score'], popular['num_comments'], color='orange', label='Popular', alpha=0.6)
    plt.scatter(non_popular['score'], non_popular['num_comments'], color='blue', label='Non-Popular', alpha=0.6)
    
    plt.title('Score vs Comments')
    plt.xlabel('Upvote Score')
    plt.ylabel('Number of Comments')
    plt.legend()
    plt.savefig('outputs/chart3_scatter.png')
    plt.show()

    # Bonus — Dashboard (+3 marks)
    # Combine all 3 into one 1x3 dashboard
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('TrendPulse Dashboard', fontsize=20)

    # Re-plot Chart 1 on Dashboard
    axes[0].barh(y_labels, top_10['score'], color='skyblue')
    axes[0].set_title('Top 10 Stories')
    axes[0].set_xlabel('Score')

    # Re-plot Chart 2 on Dashboard
    axes[1].bar(cat_counts.index, cat_counts.values, color=colors(range(len(cat_counts))))
    axes[1].set_title('Category Distribution')
    axes[1].set_xlabel('Category')

    # Re-plot Chart 3 on Dashboard
    axes[2].scatter(popular['score'], popular['num_comments'], color='orange', label='Popular', alpha=0.6)
    axes[2].scatter(non_popular['score'], non_popular['num_comments'], color='blue', label='Non-Popular', alpha=0.6)
    axes[2].set_title('Engagement Scatter')
    axes[2].set_xlabel('Score')
    axes[2].legend()

    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust to make room for suptitle
    plt.savefig('outputs/dashboard.png')
    plt.show()

    print("\n--- Pipeline Complete! ---")
    print("All charts and dashboard saved in the 'outputs/' folder.")
