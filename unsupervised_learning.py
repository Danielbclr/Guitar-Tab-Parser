import pandas as pd
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

# Load the dataset
file_path = 'output.csv'  # Update with your actual path
data = pd.read_csv(file_path)

# Drop the labels to focus on the features
X_unsupervised = data.drop(columns=['A'])

# Optional: Standardize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_unsupervised)

# Initialize a dictionary to hold the silhouette scores
clustering_results = {}

# 1. K-Means clustering
kmeans = KMeans(
    n_clusters=12, 
    n_init=20, 
    max_iter=500, 
    tol=1e-4, 
    random_state=42
)
kmeans_labels = kmeans.fit_predict(X_scaled)
kmeans_silhouette = silhouette_score(X_scaled, kmeans_labels, metric='euclidean')
clustering_results['K-means'] = kmeans_silhouette

# 2. Single-link clustering (Agglomerative with 'single' linkage method)
single_link = AgglomerativeClustering(
    n_clusters=12, 
    linkage='single', 
    metric='euclidean'
)
single_link_labels = single_link.fit_predict(X_scaled)
single_link_silhouette = silhouette_score(X_scaled, single_link_labels, metric='euclidean')
clustering_results['Single-link'] = single_link_silhouette

# 3. Average-link clustering (Agglomerative with 'average' linkage method)
average_link = AgglomerativeClustering(
    n_clusters=12, 
    linkage='average', 
    metric='manhattan'
)
average_link_labels = average_link.fit_predict(X_scaled)
average_link_silhouette = silhouette_score(X_scaled, average_link_labels, metric='manhattan')
clustering_results['Average-link'] = average_link_silhouette

# 4. Complete-link clustering (Agglomerative with 'complete' linkage method)
complete_link = AgglomerativeClustering(
    n_clusters=12, 
    linkage='complete', 
    metric='euclidean'
)
complete_link_labels = complete_link.fit_predict(X_scaled)
complete_link_silhouette = silhouette_score(X_scaled, complete_link_labels, metric='euclidean')
clustering_results['Complete-link'] = complete_link_silhouette

# Print the silhouette scores
print("Clustering Silhouette Scores:")
for method, score in clustering_results.items():
    print(f"{method}: {score:.3f}")