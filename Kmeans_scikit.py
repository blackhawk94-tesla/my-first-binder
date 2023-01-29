from sklearn.cluster import KMeans
from sklearn import datasets
from sklearn.utils import shuffle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import pandas as pd

iris = datasets.load_iris()
x = iris.data
y = iris.target

names = iris.feature_names
x,y = shuffle(x,y,random_state = 42)

model = KMeans(n_clusters=3,random_state=42)
iris_kmeans = model.fit(x)
print(iris_kmeans.labels_)

y = np.choose(y,[1,2,0]).astype(int)

print(y)

from sklearn.metrics import confusion_matrix
conf_matrix = confusion_matrix(y,iris_kmeans.labels_)
'''
fig, ax = plt.subplots(figsize=(8,6))
ax.matshow(conf_matrix,cmap = plt.cm.Blues,alpha = 0.3)
for i in range(conf_matrix.shape[0]):
    for j in range(conf_matrix.shape[1]):
        #ax.text(x = j,y =i, s = conf_matrix[i,j],va = 'center',ha = 'center',size = 'xx-large')

plt.xlabel('Predictions',fontsize = 18)
plt.ylabel('Actuals',fontsize = 18)
plt.title('Confusion Matrix',fontsize = 18)
print(plt.show())

'''

customcmap = ListedColormap(["crimson","mediumblue","darkmagenta"])
fig = plt.figure(figsize = (20,10))
ax1 = fig.add_subplot(1,2,1,projection = '3d')
#print(x[:,3].shape[0],x[:,0].shape[0],)
ax1.scatter(x[:,3],x[:,0],x[:,2],c = iris_kmeans.labels_.astype(float),edgecolor = "k",s = 150,cmap = customcmap)

ax1.view_init(20,-50)
ax1.set_xlabel(names[3],fontsize = 12)
ax1.set_ylabel(names[0],fontsize = 12)
ax1.set_zlabel(names[2],fontsize = 12)
ax1.set_title ("Kmeans Clusters for the iris Dataset",fontsize = 12)

ax2 = fig.add_subplot(1,2,2,projection = '3d')

for label, name in enumerate(['virginica','setosa','versicolor']):
    ax2.text3D(
        x[y== label,3].mean(),
        x[y == label,0].mean(),
        x[y== label,2].mean() +2,
        name,
        horizontalalignment = "center",
        bbox = dict(alpha = 0.2,edgecolor = "w",facecolor = "w"),
        )
ax2.scatter(x[:,3], x[:,0], x[:,2], c = y, edgecolor = "k", s = 150, cmap = customcmap)

ax2.view_init(20,-50)
ax2.set_xlabel(names[3],fontsize = 12)
ax2.set_ylabel(names[0],fontsize = 12)
ax2.set_zlabel(names[2],fontsize = 12)
ax2.set_title ("Actual Labels for the Iris Dataset",fontsize = 12)

print(fig.show())
#fig.savefig('temp.png')
df_iris = pd.DataFrame(x,columns = ['a1','a2','a3','a4'])
df_iris['prediction'] = y
print("Header for Iris dataset")
print(df_iris.head())
