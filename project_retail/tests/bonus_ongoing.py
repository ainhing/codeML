import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px
from sklearn.cluster import KMeans
from project_retail.connectors.connector import Connector
import webbrowser
import os

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
df2 = df2.dropna()


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
        model = KMeans(n_clusters=n, init='k-means++', max_iter=500, random_state=42)
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
    model = KMeans(n_clusters=cluster, init='k-means++', max_iter=500, random_state=42)
    model.fit(X)
    labels = model.labels_
    centroids = model.cluster_centers_
    y_kmeans = model.fit_predict(X)
    return y_kmeans, centroids, labels


X = df2.loc[:, columns].values
print(f"\nX shape: {X.shape}")
print(f"X sample:\n{X[:5]}")

cluster = 5
colors = ["red", "green", "blue", "purple", "orange"]

y_kmeans, centroids, labels = runKMeans(X, cluster)
print(f"\ny_kmeans: {y_kmeans}")
print(f"Centroids:\n{centroids}")
print(f"Labels: {labels}")

df2["cluster"] = labels


def visualizeKMeans(X, y_kmeans, cluster, title, xlabel, ylabel, colors):
    plt.figure(figsize=(10, 8))
    for i in range(cluster):
        plt.scatter(X[y_kmeans == i, 0], X[y_kmeans == i, 1], s=100, c=colors[i], label=f'Cluster {i + 1}')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()


visualizeKMeans(X, y_kmeans, cluster, "Clusters of Customers - Age X Spending Score", "Age", "Spending Score", colors)


# ============================================================================
# (1) FUNCTION TO DISPLAY CUSTOMER DETAILS BY CLUSTER ON CONSOLE
# ============================================================================
def displayCustomersByClusterConsole(df_with_clusters, conn, cluster_count):
    """
    Display detailed customer information for each cluster on the console.

    Parameters:
    - df_with_clusters: DataFrame containing CustomerId and cluster assignments
    - conn: Database connector object
    - cluster_count: Number of clusters
    """
    print("\n" + "=" * 80)
    print("CUSTOMER DETAILS BY CLUSTER (CONSOLE)")
    print("=" * 80)

    for cluster_id in range(cluster_count):
        # Get customer IDs for this cluster
        cluster_customers = df_with_clusters[df_with_clusters['cluster'] == cluster_id]
        customer_ids = cluster_customers['CustomerId'].tolist()

        print(f"\n{'=' * 80}")
        print(f"CLUSTER {cluster_id + 1} - Total Customers: {len(customer_ids)}")
        print(f"{'=' * 80}")

        if len(customer_ids) > 0:
            # Convert customer IDs to string for SQL query
            id_list = ','.join(map(str, customer_ids))

            # Query full customer details from database
            sql = f"SELECT * FROM customer WHERE CustomerId IN ({id_list})"
            customer_details = conn.queryDataset(sql)

            # Display customer details
            print(customer_details.to_string(index=False))
            print(f"\nCluster {cluster_id + 1} Statistics:")
            print(f"  - Average Age: {cluster_customers['Age'].mean():.2f}")
            if 'Annual_Income' in cluster_customers.columns:
                print(f"  - Average Annual Income: {cluster_customers['Annual_Income'].mean():.2f}")
            if 'Spending_Score' in cluster_customers.columns:
                print(f"  - Average Spending Score: {cluster_customers['Spending_Score'].mean():.2f}")
        else:
            print("No customers in this cluster.")

    print(f"\n{'=' * 80}\n")


# ============================================================================
# (2) FUNCTION TO DISPLAY CUSTOMER DETAILS BY CLUSTER ON WEB (HTML)
# ============================================================================
def displayCustomersByClusterWeb(df_with_clusters, conn, cluster_count, output_file="customer_clusters.html"):
    """
    Generate an HTML file and automatically open it in the default web browser.

    Parameters:
    - df_with_clusters: DataFrame containing CustomerId and cluster assignments
    - conn: Database connector object
    - cluster_count: Number of clusters
    - output_file: Name of the output HTML file
    """
    # Start HTML with header and navigation buttons
    html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Customer Clustering Analysis</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }
        .header {
            background-color: #4CAF50;
            color: white;
            padding: 20px;
            text-align: center;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }
        h1 {
            margin: 0;
            padding-bottom: 15px;
        }
        .button-container {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 10px;
            padding: 10px 0;
        }
        .cluster-btn {
            background-color: white;
            color: #4CAF50;
            border: 2px solid white;
            padding: 12px 24px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .cluster-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            background-color: #f1f1f1;
        }
        .cluster-btn.active {
            background-color: #2196F3;
            color: white;
            border-color: #2196F3;
        }
        .show-all-btn {
            background-color: #FF9800;
            color: white;
        }
        .show-all-btn:hover {
            background-color: #F57C00;
        }
        .content-container {
            max-width: 1400px;
            margin: 20px auto;
            padding: 0 20px;
        }
        .cluster-section {
            display: none;
            margin: 20px 0;
            padding: 20px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            animation: fadeIn 0.5s;
        }
        .cluster-section.active {
            display: block;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .cluster-header {
            background-color: #2196F3;
            color: white;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 15px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }
        th {
            background-color: #4CAF50;
            color: white;
            padding: 12px;
            text-align: left;
            position: sticky;
            top: 120px;
            z-index: 10;
        }
        td {
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tr:hover {
            background-color: #e8f5e9;
        }
        .stats {
            background-color: #e3f2fd;
            padding: 15px;
            border-radius: 5px;
            margin-top: 15px;
        }
        .stats h3 {
            margin-top: 0;
            color: #1976D2;
        }
        .stats-item {
            display: inline-block;
            margin-right: 30px;
            margin-bottom: 10px;
            font-weight: bold;
            color: #1976D2;
            font-size: 16px;
        }
    </style>
    <script>
        function showCluster(clusterNum) {
            var sections = document.getElementsByClassName('cluster-section');
            for (var i = 0; i < sections.length; i++) {
                sections[i].classList.remove('active');
            }

            var buttons = document.getElementsByClassName('cluster-btn');
            for (var i = 0; i < buttons.length; i++) {
                buttons[i].classList.remove('active');
            }

            if (clusterNum === 'all') {
                for (var i = 0; i < sections.length; i++) {
                    sections[i].classList.add('active');
                }
                document.getElementById('btn-all').classList.add('active');
            } else {
                document.getElementById('cluster-' + clusterNum).classList.add('active');
                document.getElementById('btn-' + clusterNum).classList.add('active');
            }

            window.scrollTo({top: 0, behavior: 'smooth'});
        }

        window.onload = function() {
            showCluster(0);
        };
    </script>
</head>
<body>
    <div class="header">
        <h1>🎯 Customer Clustering Analysis Report</h1>
        <div class="button-container">
"""

    # Add buttons for each cluster
    for cluster_id in range(cluster_count):
        html_content += f'            <button class="cluster-btn" id="btn-{cluster_id}" onclick="showCluster({cluster_id})">Cluster {cluster_id + 1}</button>\n'

    # Add "Show All" button
    html_content += '            <button class="cluster-btn show-all-btn" id="btn-all" onclick="showCluster(\'all\')">📋 Show All</button>\n'
    html_content += """        </div>
    </div>
    <div class="content-container">
"""

    # Generate content for each cluster
    for cluster_id in range(cluster_count):
        cluster_customers = df_with_clusters[df_with_clusters['cluster'] == cluster_id]
        customer_ids = cluster_customers['CustomerId'].tolist()

        html_content += f'        <div class="cluster-section" id="cluster-{cluster_id}">\n'
        html_content += f'            <div class="cluster-header">\n'
        html_content += f'                <h2>📊 Cluster {cluster_id + 1} - Total Customers: {len(customer_ids)}</h2>\n'
        html_content += '            </div>\n'

        if len(customer_ids) > 0:
            id_list = ','.join(map(str, customer_ids))
            sql = f"SELECT * FROM customer WHERE CustomerId IN ({id_list})"
            customer_details = conn.queryDataset(sql)

            # Create table
            html_content += '            <table>\n'
            html_content += '                <tr>'
            for col in customer_details.columns:
                html_content += f'<th>{col}</th>'
            html_content += '</tr>\n'

            for idx, row in customer_details.iterrows():
                html_content += '                <tr>'
                for col in customer_details.columns:
                    html_content += f'<td>{row[col]}</td>'
                html_content += '</tr>\n'

            html_content += '            </table>\n'

            # Add statistics
            html_content += '            <div class="stats">\n'
            html_content += '                <h3>📈 Cluster Statistics:</h3>\n'
            html_content += f'                <div class="stats-item">👤 Average Age: {cluster_customers["Age"].mean():.2f}</div>\n'
            if 'Annual_Income' in cluster_customers.columns:
                html_content += f'                <div class="stats-item">💰 Average Annual Income: ${cluster_customers["Annual_Income"].mean():.2f}</div>\n'
            if 'Spending_Score' in cluster_customers.columns:
                html_content += f'                <div class="stats-item">🛒 Average Spending Score: {cluster_customers["Spending_Score"].mean():.2f}</div>\n'
            html_content += '            </div>\n'
        else:
            html_content += '            <p>No customers in this cluster.</p>\n'

        html_content += '        </div>\n'

    html_content += """    </div>
</body>
</html>
"""

    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # Get absolute path
    abs_path = os.path.abspath(output_file)

    print(f"\n{'=' * 80}")
    print(f"✅ HTML report generated successfully!")
    print(f"📁 Location: {abs_path}")
    print(f"🌐 Opening in browser...")
    print(f"{'=' * 80}\n")

    # Try to open in browser
    try:
        webbrowser.open('file:///' + abs_path.replace('\\', '/'))
    except:
        try:
            webbrowser.open_new_tab(abs_path)
        except:
            print(f"⚠️ Could not auto-open browser. Please manually open: {abs_path}")


# ============================================================================
# INVOKE FUNCTIONS FOR SCENARIO 1: Age X Spending Score (5 clusters)
# ============================================================================
print("\n" + "#" * 80)
print("SCENARIO 1: Age X Spending Score Clustering")
print("#" * 80)
displayCustomersByClusterConsole(df2, conn, cluster)
displayCustomersByClusterWeb(df2, conn, cluster, "clusters_age_spending.html")

# ============================================================================
# SCENARIO 2: Annual Income X Spending Score
# ============================================================================
columns = ['Annual_Income', 'Spending_Score']
elbowMethod(df2, columns)

X = df2.loc[:, columns].values
cluster = 5

y_kmeans, centroids, labels = runKMeans(X, cluster)
print(f"\ny_kmeans: {y_kmeans}")
print(f"Centroids:\n{centroids}")
print(f"Labels: {labels}")

df2["cluster"] = labels

visualizeKMeans(X, y_kmeans, cluster, "Clusters of Customers - Annual Income X Spending Score",
                "Annual Income", "Spending Score", colors)

print("\n" + "#" * 80)
print("SCENARIO 2: Annual Income X Spending Score Clustering")
print("#" * 80)
displayCustomersByClusterConsole(df2, conn, cluster)
displayCustomersByClusterWeb(df2, conn, cluster, "clusters_income_spending.html")

# ============================================================================
# SCENARIO 3: Age X Annual Income X Spending Score (3D)
# ============================================================================
columns = ['Age', 'Annual_Income', 'Spending_Score']
elbowMethod(df2, columns)

X = df2.loc[:, columns].values
cluster = 6
colors_6 = ["red", "green", "blue", "purple", "orange", "cyan"]

y_kmeans, centroids, labels = runKMeans(X, cluster)
print(y_kmeans)
print(centroids)
print(labels)

df2["cluster"] = labels
print(df2)


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

print("\n" + "#" * 80)
print("SCENARIO 3: 3D Clustering (Age X Annual Income X Spending Score)")
print("#" * 80)
displayCustomersByClusterConsole(df2, conn, cluster)
displayCustomersByClusterWeb(df2, conn, cluster, "clusters_3d_all_features.html")

print("\n" + "=" * 80)
print("✨ ALL SCENARIOS COMPLETED!")
print("=" * 80)
print("📊 Three HTML reports have been generated:")
print("   1. clusters_age_spending.html")
print("   2. clusters_income_spending.html")
print("   3. clusters_3d_all_features.html")
print("=" * 80)