import pandas as pd
import pickle


# Load the precomputed interaction matrix and user similarity matrix from pickle files
with open('./interaction_matrix.pkl', 'rb') as f:
    interaction_matrix = pickle.load(f)

with open('./user_similarity_matrix.pkl', 'rb') as f:
    user_similarity_df = pickle.load(f)

# Load the expanded dataset (optional if needed for interaction details)
df_expanded = pd.read_csv('./expanded_dataset.csv')

# Interaction data for reference in recommendations
interaction_data = df_expanded[['UserId', 'History']].copy()
interaction_data.columns = ['UserId', 'NewsId']  # Ensure consistency with column names

# Step 4: Function to find similar users
def find_similar_users(user_id, user_similarity_df, interaction_matrix, top_n=5):
    """
    Function to find similar users based on user similarity matrix.
    
    Args:
    - user_id: ID of the target user
    - user_similarity_df: DataFrame with user similarity scores
    - interaction_matrix: The interaction matrix used for recommendation
    - top_n: The number of top similar users to return
    
    Returns:
    - A list of similar user IDs
    """
    if user_id not in user_similarity_df.index:
        return []

    # Get top N similar users, excluding the user themselves
    similar_users = user_similarity_df[user_id].sort_values(ascending=False).drop(user_id).head(top_n)
    return similar_users.index.tolist()

# Step 5: Recommend articles based on user similarity
def recommend_articles(user_id, threshold=1, top_n=5):
    """
    Function to recommend articles to a user based on the activity of similar users.
    
    Args:
    - user_id: ID of the target user
    - threshold: Minimum number of common articles shared between target and similar users
    - top_n: Number of top similar users to consider for recommendations
    
    Returns:
    - A set of recommended article IDs
    """
    # Get similar users
    similar_users = find_similar_users(user_id, user_similarity_df, interaction_matrix, top_n)
    
    # If no similar users found, return empty recommendations
    if not similar_users:
        print(f"No similar users found for user {user_id}")
        return set()

    recommendations = set()
    
    # Iterate through similar users to gather unread articles
    for similar_user in similar_users:
        # Get the articles the similar user has read
        similar_user_articles = set(interaction_data[interaction_data['UserId'] == similar_user]['NewsId'])
        target_user_articles = set(interaction_data[interaction_data['UserId'] == user_id]['NewsId'])

        # Find unread articles by the target user
        unread_articles = similar_user_articles - target_user_articles
        
        # Recommend if similar users have read at least the threshold of common articles
        if len(target_user_articles & similar_user_articles) >= threshold:
            recommendations.update(unread_articles)
    
    # Return the unique list of recommendations
    return recommendations

'''
# Example usage
user_id = 'U52513'

# Step 6: Get and display similar users
similar_users = find_similar_users(user_id, user_similarity_df, interaction_matrix)
print("\nSimilar Users for {}: \n".format(user_id))
print(similar_users)

# Step 7: Get article recommendations for the user
recommendations_for_user = recommend_articles(user_id, threshold=1, top_n=5)

# Get the count of recommendations
recommendation_count = len(recommendations_for_user)

# Print recommendations along with their count
print(f"\nRecommendations for {user_id}: {recommendations_for_user}")
print(f"Total number of recommendations: {recommendation_count}")
'''

train_merged = pd.read_csv('./part-dataset.csv')

# Determine the unique categories
unique_categories = train_merged['Category'].unique()

# Save unique categories for user selection
categories_df = pd.DataFrame(unique_categories, columns=['Category'])
def recommend_news_for_coldstart(favorite_categories):
    all_recommended_articles = pd.DataFrame()

    for category in favorite_categories:
        # Filter news for the current category
        filtered_news = train_merged[train_merged['Category'] == category]

        # Randomly select 5 news articles or less if not enough articles
        recommended_articles = filtered_news.sample(n=min(5, len(filtered_news)), random_state=1)

        # Append recommendations to the final list
        all_recommended_articles = pd.concat([all_recommended_articles, recommended_articles])

    return all_recommended_articles['NewsId'].tolist()
    
