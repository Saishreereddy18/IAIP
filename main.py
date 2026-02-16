# ==========================
# SUPERMARKET SALES DATA CLUSTERING
# ==========================

# Step 1: Import Libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Step 2: Open file dialog to select CSV
Tk().withdraw()  # Hide tkinter small window
file_path = askopenfilename(
    title="Select your SuperStoreOrders CSV file",
    filetypes=[("CSV Files", "*.csv")]
)

# Step 3: Load CSV
if file_path:
    df = pd.read_csv(file_path)
    print(f"Loaded file: {file_path}")
    print("First 5 rows of your data:")
    print(df.head())
else:
    print("No file selected. Please run the script again and select a CSV file.")
    exit()

# Step 4: Clean numeric columns
df['sales'] = pd.to_numeric(df['sales'], errors='coerce')  # Convert sales to numbers
df_clean = df.dropna(subset=['sales', 'quantity'])         # Remove rows with NaN

# Step 5: Select features for clustering
X = df_clean[['quantity', 'sales']]

# Step 6: Scale the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 7: Elbow Method to find optimal clusters
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=42)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)

plt.figure(figsize=(8,5))
plt.plot(range(1, 11), wcss, marker='o')
plt.title('Elbow Method for Sales Data')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

# Step 8: Apply KMeans (replace 4 with your elbow choice)
kmeans = KMeans(n_clusters=4, random_state=42)
df_clean['Cluster'] = kmeans.fit_predict(X_scaled)

# Step 9: Label clusters as High / Medium / Low Sales
# Determine which cluster is high, medium, low by looking at average sales
cluster_avg = df_clean.groupby('Cluster')['sales'].mean().sort_values(ascending=False)
cluster_mapping = {cluster: label for cluster, label in zip(cluster_avg.index, ["High Sales", "Medium Sales", "Low Sales", "Very Low Sales"])}
df_clean['Cluster_Label'] = df_clean['Cluster'].map(cluster_mapping)

# Step 10: Print cluster information
print("\nCluster Counts:")
print(df_clean['Cluster_Label'].value_counts())

print("\nAverage Quantity and Sales per Cluster:")
print(df_clean.groupby('Cluster_Label')[['quantity', 'sales']].mean())

# Step 11: Scatterplot
plt.figure(figsize=(8,6))
sns.scatterplot(
    x='quantity',
    y='sales',
    hue='Cluster_Label',
    data=df_clean,
    palette='Set1',
    s=100
)
plt.title('Sales Clusters')
plt.show()

# Step 12: Boxplots
plt.figure(figsize=(12,5))
plt.subplot(1,2,1)
sns.boxplot(x='Cluster_Label', y='quantity', data=df_clean)
plt.title('Quantity Sold by Cluster')

plt.subplot(1,2,2)
sns.boxplot(x='Cluster_Label', y='sales', data=df_clean)
plt.title('Sales by Cluster')
plt.show()

# Step 13 (Optional): Save final data with cluster labels
df_clean.to_csv("SuperStoreOrders_Clustered.csv", index=False)
print("\nFinal data saved as SuperStoreOrders_Clustered.csv")
