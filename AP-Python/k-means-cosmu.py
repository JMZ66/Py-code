import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans

# 加载数据
customers = pd.read_csv('Data/customers.csv')

# 可视化数据
points = customers.iloc[:, 3:5].values  # 年收入和消费得分
x = points[:, 0]  # 年收入
y = points[:, 1]  # 消费得分
plt.scatter(x, y, s=50, alpha=0.7)
plt.xlabel('Annual Income (k$)')
plt.ylabel('Spending Score')
plt.show()

# 使用k-means进行聚类
kmeans = KMeans(n_clusters=5, random_state=0)
kmeans.fit(points)
predicted_cluster_indexes = kmeans.predict(points)

# 绘制聚类结果
plt.scatter(x, y, c=predicted_cluster_indexes, s=50, alpha=0.7, cmap='viridis')
plt.xlabel('Annual Income (k$)')
plt.ylabel('Spending Score')

# 绘制每个簇的质心
centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='red', s=100)
plt.show()

# 识别高收入低消费客户
df = customers.copy()
df['Cluster'] = kmeans.predict(points)
cluster = kmeans.predict(np.array([[120, 20]]))[0]
clustered_df = df[df['Cluster'] == cluster]
print(clustered_df['CustomerID'].values)
