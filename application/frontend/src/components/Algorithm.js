import React from 'react';
import './css/Algorithm.css'; // Assuming you will create a separate CSS file for styling

const Algorithm = () => {
    return (
        <div className="algorithm-container">
            <h1>Algorithm Overview for User-Based Collaborative Filtering</h1>
            <p>
                The collaborative filtering approach aims to recommend items (in this case, news articles) to users by leveraging the interactions and preferences of similar users. This process involves creating an interaction matrix, calculating user similarity based on that matrix, and making recommendations from the unseen articles of similar users.
            </p>
            
            <h2>Steps Involved</h2>
            <h3>Step 1: Data Preparation</h3>
            <ul>
                <li>
                    <strong>Expand 'History' into individual rows:</strong> Each user might have interacted with multiple news articles. The 'History' column contains these article IDs in a comma-separated format. We first split the 'History' and then explode the DataFrame so that each row corresponds to a single interaction of a user with a specific article.
                </li>
                <li>
                    <strong>Create interaction data:</strong> After exploding, we create a simplified interaction_data DataFrame that consists of UserId and the articles they interacted with (represented by NewsId).
                </li>
            </ul>

            <h3>Step 2: Creating the Interaction Matrix</h3>
            <p>
                <strong>Interaction Matrix:</strong> The interaction matrix is a 2D table where rows represent users, columns represent articles (news IDs), and the values represent whether a user has interacted with a particular article (1 for interaction, 0 for no interaction).
            </p>
            <p>
                To create this, we use <code>pivot_table()</code> which transforms the interaction_data DataFrame into a matrix where:
            </p>
            <ul>
                <li>Index: User IDs</li>
                <li>Columns: News IDs (articles)</li>
                <li>Values: Interactions (1 or 0 based on whether the user read the article)</li>
            </ul>

            <h3>Step 3: Calculating Cosine Similarity Between Users</h3>
            <p>
                <strong>Cosine Similarity:</strong> Cosine similarity is a metric used to measure how similar two users are based on their interaction history. It ranges from 0 to 1, where 1 means the users have identical interaction patterns and 0 means they share no common interactions.
            </p>
            <p>
                For two users <code>A</code> and <code>B</code>, cosine similarity is calculated as:
            </p>
            <p>
                <code>similarity(A, B) = A ⋅ B / (||A|| * ||B||)</code>
            </p>
            <p>Where:</p>
            <ul>
                <li><code>A</code> and <code>B</code> are vectors representing user interactions with news articles.</li>
                <li><code>A ⋅ B</code> is the dot product of the vectors, and <code>||A||</code>, <code>||B||</code> are the magnitudes (Euclidean norms) of the vectors.</li>
            </ul>
            <p>
                The cosine similarity for all pairs of users is calculated using <code>cosine_similarity(interaction_matrix)</code> from scikit-learn, which outputs a matrix where:
            </p>
            <ul>
                <li>Rows and columns represent users.</li>
                <li>Values represent the similarity score between two users.</li>
            </ul>

            <h3>Step 4: Finding Similar Users</h3>
            <p>
                <strong>Find Top N Similar Users:</strong> For any given user, we can find their top-N similar users based on the similarity scores stored in the <code>user_similarity_df</code> DataFrame. These are sorted in descending order of similarity.
            </p>
            <p>
                We exclude the user themselves (as they have a similarity score of 1 with themselves). The function <code>find_similar_users(user_id, user_similarity_df, interaction_matrix, top_n=5)</code> identifies these top similar users for a given user.
            </p>

            <h3>Step 5: Recommending Articles Based on User Similarity</h3>
            <p>
                <strong>Recommend Articles:</strong> Using the top similar users, we recommend articles by leveraging the interaction histories:
            </p>
            <ul>
                <li>For a target user <code>U</code>, find the users who have a high similarity score with <code>U</code>.</li>
                <li>For each similar user: Identify the articles that the similar user has read but <code>U</code> hasn't.</li>
                <li>If the similar user and the target user have interacted with a threshold number of common articles, recommend those unseen articles from the similar user to the target user.</li>
            </ul>
            <p>
                The <code>recommend_articles(user_id, threshold=1)</code> function performs this step by comparing the interaction history of the target user with similar users and suggesting articles the target user hasn’t yet seen.
            </p>

            <h2>How the Interaction Matrix and User Similarity are Calculated</h2>
            <h3>Interaction Matrix Calculation:</h3>
            <p>
                <strong>Input:</strong> interaction_data: Data with two columns (UserId, NewsId) representing which users have interacted with which articles.
            </p>
            <p>
                <strong>Pivoting to Create Matrix:</strong> Each row represents a user and each column represents an article (NewsId). The values (1 or 0) indicate whether the user interacted with the article.
            </p>
            <pre>
                <code>
                    NewsId     A001    A002    A003    A004
                    UserId
                    U001         1       1       0       0
                    U002         0       1       1       1
                    U003         1       0       1       0
                </code>
            </pre>

            <h3>User Similarity Calculation:</h3>
            <p>
                <strong>Input:</strong> interaction_matrix: Matrix where rows are users and columns are articles, with values indicating user interactions.
            </p>
            <p>
                <strong>Cosine Similarity:</strong> For each pair of users, calculate the cosine similarity between their interaction vectors (rows of the matrix). The resulting matrix is symmetric and contains similarity scores between users.
            </p>
            <pre>
                <code>
                    Similarity Matrix
                            U001     U002     U003
                    U001    1.000    0.707    0.500
                    U002    0.707    1.000    0.866
                    U003    0.500    0.866    1.000
                </code>
            </pre>

            <h3>Making Predictions:</h3>
            <p>
                Once we have the similarity scores and the articles read by similar users, recommendations can be made based on the articles read by these similar users but not yet read by the target user.
            </p>
        </div>
    );
};

export default Algorithm;
