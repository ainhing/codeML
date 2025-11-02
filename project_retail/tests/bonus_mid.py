import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px
from sklearn.cluster import KMeans
from project_retail.connectors.connector import Connector
import webbrowser
import os
import pandas as pd

# ============================================================================
# KẾT NỐI DATABASE SAKILA
# ============================================================================
conn = Connector(database="sakila")
conn.connect()

# ============================================================================
# (1) PHÂN LOẠI KHÁCH HÀNG THEO TÊN PHIM
# ============================================================================
print("\n" + "=" * 80)
print("(1) PHÂN LOẠI KHÁCH HÀNG THEO TÊN PHIM")
print("=" * 80)

sql_film = """
SELECT 
    f.film_id,
    f.title AS film_title,
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    COUNT(r.rental_id) AS rental_count
FROM film f
INNER JOIN inventory i ON f.film_id = i.film_id
INNER JOIN rental r ON i.inventory_id = r.inventory_id
INNER JOIN customer c ON r.customer_id = c.customer_id
GROUP BY f.film_id, f.title, c.customer_id, c.first_name, c.last_name
ORDER BY f.title, rental_count DESC
"""

df_film = conn.queryDataset(sql_film)
print(df_film.head(20))
print(f"\nTotal records: {len(df_film)}")

# ============================================================================
# (2) PHÂN LOẠI KHÁCH HÀNG THEO CATEGORY
# ============================================================================
print("\n" + "=" * 80)
print("(2) PHÂN LOẠI KHÁCH HÀNG THEO CATEGORY")
print("=" * 80)

sql_category = """
SELECT 
    cat.category_id,
    cat.name AS category_name,
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    COUNT(DISTINCT r.rental_id) AS rental_count,
    COUNT(DISTINCT f.film_id) AS distinct_films_rented
FROM category cat
INNER JOIN film_category fc ON cat.category_id = fc.category_id
INNER JOIN film f ON fc.film_id = f.film_id
INNER JOIN inventory i ON f.film_id = i.film_id
INNER JOIN rental r ON i.inventory_id = r.inventory_id
INNER JOIN customer c ON r.customer_id = c.customer_id
GROUP BY cat.category_id, cat.name, c.customer_id, c.first_name, c.last_name
ORDER BY cat.name, rental_count DESC
"""

df_category = conn.queryDataset(sql_category)
print(df_category.head(20))
print(f"\nTotal records: {len(df_category)}")

# ============================================================================
# (3) XEM XÉT CÁC BẢNG DỮ LIỆU
# ============================================================================
print("\n" + "=" * 80)
print("(3) XEM XÉT CÁC BẢNG DỮ LIỆU")
print("=" * 80)

# Customer table
sql_customer = "SELECT * FROM customer LIMIT 10"
df_customer_sample = conn.queryDataset(sql_customer)
print("\nCUSTOMER TABLE (Sample):")
print(df_customer_sample)

# Inventory table
sql_inventory = "SELECT * FROM inventory LIMIT 10"
df_inventory_sample = conn.queryDataset(sql_inventory)
print("\nINVENTORY TABLE (Sample):")
print(df_inventory_sample)

# Rental table
sql_rental = "SELECT * FROM rental LIMIT 10"
df_rental_sample = conn.queryDataset(sql_rental)
print("\nRENTAL TABLE (Sample):")
print(df_rental_sample)

# Film table
sql_film_table = "SELECT * FROM film LIMIT 10"
df_film_sample = conn.queryDataset(sql_film_table)
print("\nFILM TABLE (Sample):")
print(df_film_sample)

# ============================================================================
# TẠO DATASET CHO K-MEANS CLUSTERING
# Gom cụm khách hàng về mức độ quan tâm Film và Inventory
# ============================================================================
print("\n" + "=" * 80)
print("CHUẨN BỊ DỮ LIỆU CHO K-MEANS CLUSTERING")
print("=" * 80)

sql_kmeans = """
SELECT 
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.email,
    c.active,
    COUNT(r.rental_id) AS total_rentals,
    COUNT(DISTINCT f.film_id) AS unique_films_rented,
    COUNT(DISTINCT cat.category_id) AS unique_categories,
    COALESCE(AVG(f.rental_rate), 0) AS avg_rental_rate,
    COALESCE(AVG(f.length), 0) AS avg_film_length,
    COALESCE(SUM(p.amount), 0) AS total_payment,
    COALESCE(AVG(p.amount), 0) AS avg_payment_per_rental,
    COUNT(DISTINCT DATE(r.rental_date)) AS rental_days_count
FROM customer c
LEFT JOIN rental r ON c.customer_id = r.customer_id
LEFT JOIN inventory i ON r.inventory_id = i.inventory_id
LEFT JOIN film f ON i.film_id = f.film_id
LEFT JOIN film_category fc ON f.film_id = fc.film_id
LEFT JOIN category cat ON fc.category_id = cat.category_id
LEFT JOIN payment p ON r.rental_id = p.rental_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.email, c.active
ORDER BY total_rentals DESC
"""

df_kmeans = conn.queryDataset(sql_kmeans)
print(df_kmeans.head())
print(f"\nDataset shape: {df_kmeans.shape}")
print(f"\nDataset info:")
print(df_kmeans.describe())

# Kiểm tra và xử lý null
print(f"\nNull values:\n{df_kmeans.isnull().sum()}")
df_kmeans = df_kmeans.dropna()


# ============================================================================
# VISUALIZE HISTOGRAMS
# ============================================================================
def showHistogram(df, columns, title_prefix=""):
    n_cols = len(columns)
    plt.figure(figsize=(15, 4 * ((n_cols + 2) // 3)))

    for idx, column in enumerate(columns, 1):
        plt.subplot((n_cols + 2) // 3, 3, idx)
        plt.subplots_adjust(hspace=0.4, wspace=0.3)
        sns.histplot(df[column], bins=20, kde=True)
        plt.title(f'{title_prefix}Histogram of {column}')
    plt.show()


# Hiển thị histogram cho các features quan trọng
numeric_columns = ['total_rentals', 'unique_films_rented', 'unique_categories',
                   'avg_rental_rate', 'avg_film_length', 'total_payment']
showHistogram(df_kmeans, numeric_columns, "Sakila - ")


# ============================================================================
# ELBOW METHOD
# ============================================================================
def elbowMethod(df, columnsForElbow, title="Elbow Method"):
    X = df.loc[:, columnsForElbow].values
    inertia = []
    for n in range(1, 11):
        model = KMeans(n_clusters=n, init='k-means++', max_iter=500, random_state=42)
        model.fit(X)
        inertia.append(model.inertia_)

    plt.figure(figsize=(12, 6))
    plt.plot(np.arange(1, 11), inertia, 'o-', linewidth=2, markersize=8)
    plt.xlabel('Number of Clusters', fontsize=12)
    plt.ylabel('Inertia (Within-cluster sum of squares)', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.show()


# ============================================================================
# K-MEANS CLUSTERING FUNCTION
# ============================================================================
def runKMeans(X, cluster):
    model = KMeans(n_clusters=cluster, init='k-means++', max_iter=500, random_state=42)
    model.fit(X)
    labels = model.labels_
    centroids = model.cluster_centers_
    y_kmeans = model.fit_predict(X)
    return y_kmeans, centroids, labels


# ============================================================================
# VISUALIZATION FUNCTION
# ============================================================================
def visualizeKMeans(X, y_kmeans, cluster, title, xlabel, ylabel, colors):
    plt.figure(figsize=(12, 8))
    for i in range(cluster):
        plt.scatter(X[y_kmeans == i, 0], X[y_kmeans == i, 1],
                    s=100, c=colors[i], label=f'Cluster {i + 1}', alpha=0.6)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()


# ============================================================================
# SCENARIO 1: Total Rentals X Total Payment
# ============================================================================
print("\n" + "#" * 80)
print("SCENARIO 1: Clustering - Total Rentals X Total Payment")
print("#" * 80)

columns_s1 = ['total_rentals', 'total_payment']
elbowMethod(df_kmeans, columns_s1, "Elbow Method: Total Rentals X Total Payment")

X_s1 = df_kmeans.loc[:, columns_s1].values
cluster_s1 = 5
colors = ["red", "green", "blue", "purple", "orange"]

y_kmeans_s1, centroids_s1, labels_s1 = runKMeans(X_s1, cluster_s1)
df_kmeans["cluster_s1"] = labels_s1

visualizeKMeans(X_s1, y_kmeans_s1, cluster_s1,
                "Customer Clusters: Total Rentals vs Total Payment",
                "Total Rentals", "Total Payment ($)", colors)

# ============================================================================
# SCENARIO 2: Unique Films X Unique Categories
# ============================================================================
print("\n" + "#" * 80)
print("SCENARIO 2: Clustering - Unique Films X Unique Categories")
print("#" * 80)

columns_s2 = ['unique_films_rented', 'unique_categories']
elbowMethod(df_kmeans, columns_s2, "Elbow Method: Unique Films X Unique Categories")

X_s2 = df_kmeans.loc[:, columns_s2].values
cluster_s2 = 4

y_kmeans_s2, centroids_s2, labels_s2 = runKMeans(X_s2, cluster_s2)
df_kmeans["cluster_s2"] = labels_s2

colors_s2 = ["red", "green", "blue", "purple"]
visualizeKMeans(X_s2, y_kmeans_s2, cluster_s2,
                "Customer Clusters: Unique Films vs Categories Diversity",
                "Unique Films Rented", "Unique Categories", colors_s2)

# ============================================================================
# SCENARIO 3: 3D Clustering - Total Rentals X Unique Films X Total Payment
# ============================================================================
print("\n" + "#" * 80)
print("SCENARIO 3: 3D Clustering - Rentals X Films X Payment")
print("#" * 80)

columns_s3 = ['total_rentals', 'unique_films_rented', 'total_payment']
elbowMethod(df_kmeans, columns_s3, "Elbow Method: 3D Clustering")

X_s3 = df_kmeans.loc[:, columns_s3].values
cluster_s3 = 5

y_kmeans_s3, centroids_s3, labels_s3 = runKMeans(X_s3, cluster_s3)
df_kmeans["cluster_s3"] = labels_s3


def visualize3DKmeans(df, columns, hover_data, cluster, title="3D Clustering"):
    fig = px.scatter_3d(
        df,
        x=columns[0],
        y=columns[1],
        z=columns[2],
        color='cluster_s3',
        hover_data=hover_data,
        title=title,
        labels={columns[0]: columns[0].replace('_', ' ').title(),
                columns[1]: columns[1].replace('_', ' ').title(),
                columns[2]: columns[2].replace('_', ' ').title()},
        category_orders={"cluster_s3": range(0, cluster)},
    )
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=40))
    fig.show()


hover_data = ['customer_name', 'email', 'total_rentals', 'unique_films_rented',
              'unique_categories', 'total_payment']
visualize3DKmeans(df_kmeans, columns_s3, hover_data, cluster_s3,
                  "3D Customer Clustering: Rentals × Films × Payment")


# ============================================================================
# DISPLAY FUNCTIONS - CONSOLE
# ============================================================================
def displayCustomersByClusterConsole(df_with_clusters, conn, cluster_count, cluster_col='cluster_s1'):
    print("\n" + "=" * 80)
    print(f"CUSTOMER DETAILS BY CLUSTER - {cluster_col.upper()}")
    print("=" * 80)

    for cluster_id in range(cluster_count):
        cluster_customers = df_with_clusters[df_with_clusters[cluster_col] == cluster_id]
        customer_ids = cluster_customers['customer_id'].tolist()

        print(f"\n{'=' * 80}")
        print(f"CLUSTER {cluster_id + 1} - Total Customers: {len(customer_ids)}")
        print(f"{'=' * 80}")

        if len(customer_ids) > 0:
            id_list = ','.join(map(str, customer_ids))
            sql = f"""
            SELECT c.customer_id, c.first_name, c.last_name, c.email, 
                   c.active, a.address, ci.city, co.country
            FROM customer c
            LEFT JOIN address a ON c.address_id = a.address_id
            LEFT JOIN city ci ON a.city_id = ci.city_id
            LEFT JOIN country co ON ci.country_id = co.country_id
            WHERE c.customer_id IN ({id_list})
            """
            customer_details = conn.queryDataset(sql)
            print(customer_details.to_string(index=False))

            print(f"\nCluster {cluster_id + 1} Statistics:")
            print(f"  - Average Total Rentals: {cluster_customers['total_rentals'].mean():.2f}")
            print(f"  - Average Unique Films: {cluster_customers['unique_films_rented'].mean():.2f}")
            print(f"  - Average Total Payment: ${cluster_customers['total_payment'].mean():.2f}")
            print(f"  - Average Categories Explored: {cluster_customers['unique_categories'].mean():.2f}")


# ============================================================================
# DISPLAY FUNCTIONS - WEB HTML
# ============================================================================
def displayCustomersByClusterWeb(df_with_clusters, conn, cluster_count,
                                 cluster_col='cluster_s1',
                                 output_file="sakila_clusters.html",
                                 scenario_title="Customer Clustering"):
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Sakila - {scenario_title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            position: sticky;
            top: 0;
            z-index: 1000;
        }}
        h1 {{
            margin: 0;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .subtitle {{
            margin-top: 10px;
            font-size: 1.2em;
            opacity: 0.9;
        }}
        .button-container {{
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 15px;
            margin-top: 20px;
        }}
        .cluster-btn {{
            background-color: white;
            color: #667eea;
            border: none;
            padding: 12px 30px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 30px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .cluster-btn:hover {{
            transform: translateY(-3px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.2);
        }}
        .cluster-btn.active {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }}
        .show-all-btn {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
        }}
        .content-container {{
            max-width: 1400px;
            margin: 30px auto;
            padding: 0 20px;
        }}
        .cluster-section {{
            display: none;
            margin: 20px 0;
            padding: 30px;
            background-color: white;
            border-radius: 15px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
            animation: fadeIn 0.5s;
        }}
        .cluster-section.active {{
            display: block;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .cluster-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: bold;
        }}
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e0e0e0;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        tr:hover {{
            background-color: #e3f2fd;
            transition: background-color 0.2s;
        }}
        .stats {{
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        .stats h3 {{
            margin-top: 0;
            color: #667eea;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}
        .stats-item {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stats-label {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 5px;
        }}
        .stats-value {{
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
        }}
    </style>
    <script>
        function showCluster(clusterNum) {{
            var sections = document.getElementsByClassName('cluster-section');
            for (var i = 0; i < sections.length; i++) {{
                sections[i].classList.remove('active');
            }}
            var buttons = document.getElementsByClassName('cluster-btn');
            for (var i = 0; i < buttons.length; i++) {{
                buttons[i].classList.remove('active');
            }}
            if (clusterNum === 'all') {{
                for (var i = 0; i < sections.length; i++) {{
                    sections[i].classList.add('active');
                }}
                document.getElementById('btn-all').classList.add('active');
            }} else {{
                document.getElementById('cluster-' + clusterNum).classList.add('active');
                document.getElementById('btn-' + clusterNum).classList.add('active');
            }}
            window.scrollTo({{top: 0, behavior: 'smooth'}});
        }}
        window.onload = function() {{
            showCluster(0);
        }};
    </script>
</head>
<body>
    <div class="header">
        <h1>🎬 Sakila Database Analysis</h1>
        <div class="subtitle">{scenario_title}</div>
        <div class="button-container">
"""

    for cluster_id in range(cluster_count):
        html_content += f'            <button class="cluster-btn" id="btn-{cluster_id}" onclick="showCluster({cluster_id})">Cluster {cluster_id + 1}</button>\n'

    html_content += '            <button class="cluster-btn show-all-btn" id="btn-all" onclick="showCluster(\'all\')">📋 Show All</button>\n'
    html_content += """        </div>
    </div>
    <div class="content-container">
"""

    for cluster_id in range(cluster_count):
        cluster_customers = df_with_clusters[df_with_clusters[cluster_col] == cluster_id]
        customer_ids = cluster_customers['customer_id'].tolist()

        html_content += f'        <div class="cluster-section" id="cluster-{cluster_id}">\n'
        html_content += f'            <div class="cluster-header">\n'
        html_content += f'                <h2> Cluster {cluster_id + 1} - Total Customers: {len(customer_ids)}</h2>\n'
        html_content += '            </div>\n'

        if len(customer_ids) > 0:
            id_list = ','.join(map(str, customer_ids))
            sql = f"""
            SELECT c.customer_id, c.first_name, c.last_name, c.email, 
                   c.active, a.address, ci.city, co.country
            FROM customer c
            LEFT JOIN address a ON c.address_id = a.address_id
            LEFT JOIN city ci ON a.city_id = ci.city_id
            LEFT JOIN country co ON ci.country_id = co.country_id
            WHERE c.customer_id IN ({id_list})
            """
            customer_details = conn.queryDataset(sql)

            html_content += '            <table>\n'
            html_content += '                <tr>'
            for col in customer_details.columns:
                html_content += f'<th>{col.replace("_", " ").title()}</th>'
            html_content += '</tr>\n'

            for idx, row in customer_details.iterrows():
                html_content += '                <tr>'
                for col in customer_details.columns:
                    html_content += f'<td>{row[col]}</td>'
                html_content += '</tr>\n'

            html_content += '            </table>\n'

            html_content += '            <div class="stats">\n'
            html_content += '                <h3>Cluster Statistics</h3>\n'
            html_content += '                <div class="stats-grid">\n'
            html_content += f'                    <div class="stats-item"><div class="stats-label">Avg Total Rentals</div><div class="stats-value">{cluster_customers["total_rentals"].mean():.2f}</div></div>\n'
            html_content += f'                    <div class="stats-item"><div class="stats-label">Avg Unique Films</div><div class="stats-value">{cluster_customers["unique_films_rented"].mean():.2f}</div></div>\n'
            html_content += f'                    <div class="stats-item"><div class="stats-label">Avg Total Payment</div><div class="stats-value">${cluster_customers["total_payment"].mean():.2f}</div></div>\n'
            html_content += f'                    <div class="stats-item"><div class="stats-label">Avg Categories</div><div class="stats-value">{cluster_customers["unique_categories"].mean():.2f}</div></div>\n'
            html_content += '                </div>\n'
            html_content += '            </div>\n'

        html_content += '        </div>\n'

    html_content += """    </div>
</body>
</html>
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    abs_path = os.path.abspath(output_file)
    print(f"\n{'=' * 80}")
    print(f" HTML report generated: {output_file}")
    print(f" Location: {abs_path}")
    print(f"{'=' * 80}\n")

    try:
        webbrowser.open('file:///' + abs_path.replace('\\', '/'))
    except:
        print(f" Could not auto-open browser. Please manually open: {abs_path}")


# ============================================================================
# RUN ALL SCENARIOS
# ============================================================================
print("\n" + "#" * 80)
print("GENERATING REPORTS FOR ALL SCENARIOS")
print("#" * 80)

# Scenario 1
displayCustomersByClusterConsole(df_kmeans, conn, cluster_s1, 'cluster_s1')
displayCustomersByClusterWeb(df_kmeans, conn, cluster_s1, 'cluster_s1',
                             "sakila_cluster_rentals_payment.html",
                             "Scenario 1: Total Rentals × Total Payment")

# Scenario 2
displayCustomersByClusterConsole(df_kmeans, conn, cluster_s2, 'cluster_s2')
displayCustomersByClusterWeb(df_kmeans, conn, cluster_s2, 'cluster_s2',
                             "sakila_cluster_films_categories.html",
                             "Scenario 2: Unique Films × Categories Diversity")

# Scenario 3
displayCustomersByClusterConsole(df_kmeans, conn, cluster_s3, 'cluster_s3')
displayCustomersByClusterWeb(df_kmeans, conn, cluster_s3, 'cluster_s3',
                             "sakila_cluster_3d.html",
                             "Scenario 3: 3D Clustering (Rentals × Films × Payment)")

print("\n" + "=" * 80)
print("ALL ANALYSIS COMPLETED!")
print("=" * 80)
print("Three HTML reports have been generated:")
print("   1. sakila_cluster_rentals_payment.html")
print("   2. sakila_cluster_films_categories.html")
print("   3. sakila_cluster_3d.html")
print("=" * 80)

conn.close()