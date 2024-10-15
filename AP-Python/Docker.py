from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

# 创建一些随机数据
X = np.random.rand(200, 2)

# 使用k-means进行聚类，选择3个簇
kmeans = KMeans(n_clusters=3, random_state=0).fit(X)

# 获取簇的中心点和簇的标签
centroids = kmeans.cluster_centers_
labels = kmeans.labels_

# 绘制聚类结果
plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis')
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', marker='x')
plt.show()

