import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px
from sklearn.cluster import KMeans
from project_retail.connectors.connector import Connector

# Kết nối database
conn = Connector(database="salesdatabase")
conn.connect()

# Lấy dữ liệu
sql = "select * from customer"
df = conn.queryDataset(sql)
print(df)

sql2 = ("select distinct customer.CustomerId, Age, Annual_Income, Spending_Score from customer, customer_spend_score "
        "where customer.CustomerId = customer_spend_score.CustomerID")
df2 = conn.queryDataset(sql2)
print(df2)

print(df2.head())
print(df2.describe())

# Kiểm tra và xử lý dữ liệu null
print(f"\nShape of df2: {df2.shape}")
print(f"Null values:\n{df2.isnull().sum()}")
df2 = df2.dropna()  # Xóa các dòng có giá trị null

def showHistogram(df, columns):
    plt.figure(figsize=(7, 8))
    n = 0
    for column in columns:
        n += 1
        plt.subplot(3, 1, n)
        plt.subplots_adjust(hspace=0.5, wspace=0.5)
        sns.histplot(df[column], bins=32)
        plt.title(f'Histogram of {column}')
    plt.show()

showHistogram(df2, df2.columns[1:])

def elbowMethod(df, columnsForElbow):
    X = df.loc[:, columnsForElbow].values
    inertia = []
    for n in range(1, 11):
        model = KMeans(n_clusters=n,
                       init='k-means++',
                       max_iter=500,
                       random_state=42)
        model.fit(X)
        inertia.append(model.inertia_)

    plt.figure(figsize=(15, 6))
    plt.plot(np.arange(1, 11), inertia, 'o')
    plt.plot(np.arange(1, 11), inertia, '-', alpha=0.5)
    plt.xlabel('Number of Clusters')
    plt.ylabel('Cluster sum of squared distances')
    plt.show()

columns = ['Age', 'Spending_Score']
elbowMethod(df2, columns)

def runKMeans(X, cluster):
    model = KMeans(n_clusters=cluster,
                   init='k-means++',
                   max_iter=500,
                   random_state=42)
    model.fit(X)
    labels = model.labels_
    centroids = model.cluster_centers_
    y_kmeans = model.fit_predict(X)
    return y_kmeans, centroids, labels

X = df2.loc[:, columns].values
print(f"\nX shape: {X.shape}")
print(f"X sample:\n{X[:5]}")

cluster = 5  # Chỉnh số lượng cluster phù hợp
colors = ["red", "green", "blue", "purple", "orange"]  # Cập nhật mảng màu

y_kmeans, centroids, labels = runKMeans(X, cluster)
print(f"\ny_kmeans: {y_kmeans}")
print(f"Centroids:\n{centroids}")
print(f"Labels: {labels}")

df2["cluster"] = labels

def visualizeKMeans(X, y_kmeans, cluster, title, xlabel, ylabel, colors):
    plt.figure(figsize=(10, 8))
    for i in range(cluster):
        plt.scatter(X[y_kmeans == i, 0],
                    X[y_kmeans == i, 1],
                    s=100,
                    c=colors[i],
                    label=f'Cluster {i + 1}')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()

visualizeKMeans(X,
                y_kmeans,
                cluster,
                "Clusters of Customers - Age X Spending Score",
                "Age",
                "Spending Score",
                colors)

# Xử lý thêm một tập dữ liệu khác với cột 'Annual_Income' và 'Spending_Score'
columns = ['Annual_Income', 'Spending_Score']
elbowMethod(df2, columns)

X = df2.loc[:, columns].values
cluster = 5  # Chỉnh số lượng cluster phù hợp

y_kmeans, centroids, labels = runKMeans(X, cluster)

print(f"\ny_kmeans: {y_kmeans}")
print(f"Centroids:\n{centroids}")
print(f"Labels: {labels}")

df2["cluster"] = labels

visualizeKMeans(X,
                y_kmeans,
                cluster,
                "Clusters of Customers - Annual Income X Spending Score",
                "Annual Income",
                "Spending Score",
                colors)

columns = ['Age', 'Annual_Income', 'Spending_Score']
elbowMethod(df2, columns)

X = df2.loc[:, columns].values
cluster = 6

y_kmeans, centroids, labels = runKMeans(X, cluster)

print(y_kmeans)
print(centroids)
print(labels)

df2["cluster"] = labels
print(df2)

# Hàm vẽ 3D KMeans
import plotly.express as px
def visualize3DKmeans(df, columns, hover_data, cluster):
    fig = px.scatter_3d(
        df,
        x=columns[0],
        y=columns[1],
        z=columns[2],
        color='cluster',
        hover_data=hover_data,
        category_orders={"cluster": range(0, cluster)},
    )
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    fig.show()

hover_data = df2.columns
visualize3DKmeans(df2, columns, hover_data, cluster)
