from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.preprocessing import OrdinalEncoder
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score , silhouette_samples
from tqdm import tqdm


data = pd.read_csv(r"./data/cluster_feature.csv",index_col=0)
data_ = data.copy()
# OrdinalEncoder().fit(data_.iloc[:,[8,9,10,11,14]]).categories_
# 编码
data_.iloc[:,[8,9,10,11,14]] = OrdinalEncoder().fit_transform(data_.iloc[:,[8,9,10,11,14]])
data_ = np.array(data_)
silhouette_score_max = 0
optimize_clusters = 0

for i in tqdm(range(900,1000)):
    n_clusters = i
    cluster = KMeans(n_clusters=n_clusters, random_state=10).fit(data_)
    cluster_labels = cluster.labels_
    silhouette_avg = silhouette_score(data_, cluster_labels)
    if silhouette_avg > silhouette_score_max:
        silhouette_score_max = silhouette_avg
        optimize_clusters = n_clusters
# n_clusters = 699
# cluster = KMeans(n_clusters=n_clusters, random_state=10).fit(data_)
# cluster_labels = cluster.labels_
# silhouette_avg = silhouette_score(data_, cluster_labels)
print("n_clusters:",optimize_clusters,"silhouette_score",silhouette_score_max)
