import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# Load the final dataset
final_dataset = pd.read_csv('players_salaries.csv')

# Select features for clustering
features = final_dataset[['USG%', 'Age', 'PercentSalaryCap']]

# Normalize the data
scaler = StandardScaler()
normalized_features = scaler.fit_transform(features)
# Determine the optimal number of clusters using the Elbow Method
sse = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=0)
    kmeans.fit(normalized_features)
    sse.append(kmeans.inertia_)

plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), sse, marker='o')
plt.title('Elbow Method for Optimal Number of Clusters')
plt.xlabel('Number of Clusters')
plt.ylabel('SSE')
plt.grid(True)
plt.show()

# Apply K-Means with the optimal number of clusters (e.g., k=3)
optimal_k = 6  # Assuming the optimal number of clusters is 3 based on the Elbow Method
kmeans = KMeans(n_clusters=optimal_k, random_state=0)
clusters = kmeans.fit_predict(normalized_features)

# Add cluster labels to the original dataset
final_dataset['Cluster'] = clusters

# Create a 3D scatter plot with cluster labels
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Scatter plot
sc = ax.scatter(
    final_dataset['USG%'],
    final_dataset['Age'],
    final_dataset['PercentSalaryCap'],
    c=final_dataset['Cluster'],  # Color by cluster
    cmap='viridis',
    marker='o'
)

# Add color bar which maps values to colors
cbar = plt.colorbar(sc)
cbar.set_label('Cluster')

# Set labels
ax.set_xlabel('Usage Rate')
ax.set_ylabel('Age')
ax.set_zlabel('Percent Salary Cap')

# Set title
ax.set_title('3D Scatter Plot: Usage Rate vs Age vs Percent Salary Cap (Clusters)')

plt.show()

# Calculate the mean values for each variable within each cluster
cluster_means = final_dataset.groupby('Cluster')[['USG%', 'Age', 'PercentSalaryCap']].mean()

cluster_means.to_csv('cluster_means.csv')
# Map cluster numbers to descriptive names
cluster_counts_all_seasons = final_dataset.groupby(['Season', 'Team', 'Cluster']).size().unstack(fill_value=0)
print(cluster_counts_all_seasons)
# Save the dataset with the cluster labels included
final_dataset.to_csv("Players with Clusters.csv", index=0)
cluster_counts_all_seasons.to_csv("Team Cluster Counts.csv")
# Save the cluster means to a separate CSV file
