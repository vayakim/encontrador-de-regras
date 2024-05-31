import numpy as np
from sklearn.cluster import KMeans


class clusterizacao:
    def __init__(self, data):
        self.data = data
        self.clusters = None

    def kmeans(self):
        kmeans = KMeans(n_clusters=5)
        kmeans.fit(self.data)
        self.clusters = kmeans.labels_
    
    def show_clusters(self):
        print(self.clusters)
