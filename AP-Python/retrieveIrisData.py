# 导入必要的库
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
import numpy as np


# 加载鸢尾花数据集
iris = load_iris()
X = iris.data
y = iris.target

# 创建KNeighborsClassifier实例并进行训练
knn = KNeighborsClassifier()
knn.fit(X, y)

# 使用交叉验证评估模型
scores = cross_val_score(knn, X, y, cv=5)
print("Cross - validation scores:", scores)
print("Average score:", np.mean(scores))

# 假设一个新的数据点（这里随机生成一个与鸢尾花特征维度相同的数据点）
new_data = np.array([[5.1, 3.5, 1.4, 0.2]])
new_prediction = knn.predict(new_data)
print("Prediction for new data:", new_prediction)