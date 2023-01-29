from sklearn.cluster import KMeans
from sklearn import datasets
from sklearn.utils import shuffle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import pandas as pd

iris = datasets.load_iris()
param = iris.data
label_cluster = iris.target

Groups = iris.feature_names
param, label_cluster = shuffle(param, label_cluster, random_state = 42)

model = KMeans(n_clusters=3,random_state=42)
iris_kmeans = model.fit(param)
#print(iris_kmeans.labels_)

label_cluster = np.choose(label_cluster, [1, 2, 0]).astype(int)

#print(label_cluster)

custom_mapping = ListedColormap(["crimson", "mediumblue", "darkmagenta"])
fig = plt.figure(figsize = (20,10))
ax1 = fig.add_subplot(1,2,1,projection = '3d')

ax1.scatter(param[:, 3], param[:, 0], param[:, 2], c = iris_kmeans.labels_.astype(float), edgecolor ="k", s = 150, cmap = custom_mapping)

ax1.view_init(20,-50)
ax1.set_xlabel(Groups[3], fontsize = 12)
ax1.set_ylabel(Groups[0], fontsize = 12)
ax1.set_zlabel(Groups[2], fontsize = 12)
ax1.set_title ("Kmeans Clusters for the iris Dataset",fontsize = 12)

ax2 = fig.add_subplot(1,2,2,projection = '3d')

for label, name in enumerate(['virginica','setosa','versicolor']):
    ax2.text3D(
        param[label_cluster == label, 3].mean(),
        param[label_cluster == label, 0].mean(),
        param[label_cluster == label, 2].mean() + 2,
        name,
        horizontalalignment = "center",
        bbox = dict(alpha = 0.2,edgecolor = "w",facecolor = "w"),
        )
ax2.scatter(param[:, 3], param[:, 0], param[:, 2], c = label_cluster, edgecolor ="k", s = 150, cmap = custom_mapping)

ax2.view_init(20,-50)
ax2.set_xlabel(Groups[3], fontsize = 12)
ax2.set_ylabel(Groups[0], fontsize = 12)
ax2.set_zlabel(Groups[2], fontsize = 12)
ax2.set_title ("Target Labels for the Iris Dataset",fontsize = 12)

fig.savefig('3D_clusters.png')

from sklearn.metrics import confusion_matrix
perf_matrix = confusion_matrix(label_cluster, iris_kmeans.labels_)

fig, ax = plt.subplots(figsize=(8,6))
ax.matshow(perf_matrix,cmap = plt.cm.Reds,alpha = 0.2)
for i in range(perf_matrix.shape[0]):
    for j in range(perf_matrix.shape[1]):
        ax.text(x = j,y =i, s = perf_matrix[i,j],va = 'center',ha = 'center',size = 'xx-large')

plt.xlabel('Predictions',fontsize = 18)
plt.ylabel('Targets',fontsize = 18)
plt.title('Performance Matrix',fontsize = 18)
plt.savefig('Performance_Matrix.png')

df_iris = pd.DataFrame(param, columns = ['a1', 'a2', 'a3', 'a4'])
df_iris['prediction'] = label_cluster
print("Header for Iris dataset")
print(df_iris.head())
