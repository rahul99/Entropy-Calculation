import sys
import os

import numpy as np
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from scipy.spatial import distance
from collections import defaultdict

def check_core(point_idx, X, eps, minpts):
    distances = distance.cdist([X[point_idx]], X, 'euclidean')[0]
    neighbours = list(np.where(distances <= eps)[0])

    if(len(neighbours) >= minpts):
        is_core = True
        return(is_core, neighbours)
    else:
        is_core=False
        neighbours = []
        return(is_core, neighbours)

def dbscan(X, eps, minpts):
    '''
        X (numpy.ndarray): a numpy array of points with dimension (n, d) where n is the number of points and d is the dimension of the data points
        eps (float): eps specifies the maximum distance between two samples for them to be considered as in the same neighborhood
        minpts (int): minpts is the number of samples in a neighborhood for a point to be considered as a core point. This includes the point itself.

    Returns:
        list: The output is a list of two lists, the first list contains the cluster label of each point, where -1 means that point is a noise point, the second list contains the indexes of the core points from the X array.

    Example:
        Input: X = np.array([[-10.1,-20.3], [2.0, 1.5], [4.3, 4.4], [4.3, 4.6], [4.3, 4.5], [2.0, 1.6], [2.0, 1.4]]), eps = 0.1, minpts = 3
        Output: [[-1, 1, 0, 0, 0, 1, 1], [1, 4]]
        The meaning of the output is as follows: the first list from the output tells us: X[0] is a noise point, X[1],X[5],X[6] belong to cluster 1 and X[2],X[3],X[4] belong to cluster 0; the second list tell us X[1] and X[4] are the only two core points
    '''

    cluster_label = dict()
    core_point_idx = []
    cluster_idx = []
    curr_cluster_label = -1
    visited = [] # running list of visited points:

    # Part I: Find the core points and assign labels
    for idx in range(X.shape[0]):
        if(idx in visited):
            continue
        visited.append(idx)

        is_core, neighbours = check_core(point_idx=idx, X=X, eps=eps, minpts=minpts)
        if(is_core):
            # check if label already assigned
            if(idx not in cluster_label):
                curr_cluster_label += 1
                cluster_label[idx] = curr_cluster_label

            # grow cluster
            counter=0
            while(counter < len(neighbours)):
                neighbour_idx = neighbours[counter]
                if(neighbour_idx in visited):
                    counter = counter + 1
                    continue
                visited.append(neighbour_idx)

                if(neighbour_idx not in cluster_label):
                    cluster_label[neighbour_idx] = curr_cluster_label
                    is_core, new_neighbours = check_core(point_idx=neighbour_idx, X=X, eps=eps, minpts=minpts)
                    if(is_core):
                        core_point_idx.append(idx)
                        neighbours += new_neighbours
                counter += 1

        else:
            if(idx not in cluster_label):
                cluster_label[idx] = -1


    # Part II: Convert dict to list in the same order as X
    for key in range(X.shape[0]):
        cluster_idx.append(cluster_label[key])

    return [cluster_idx, core_point_idx]


def plot_dbscan(X, db):
    core_samples_mask = np.zeros_like(np.array(db[0]), dtype=bool)
    core_samples_mask[db[1]] = True
    labels = np.array(db[0])

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(unique_labels))]

    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = (labels == k)

        xy = X[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=14)

        xy = X[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=6)

    plt.title('Estimated number of location clusters: %d' % n_clusters_)
    plt.show()


def main():
    if len(sys.argv) != 4:
        print("Wrong command format, please follwoing the command format below:")
        print("python dbscan.py data_filepath eps minpts")
        exit(0)

    X = read_data(sys.argv[1])

    # Compute DBSCAN
    db = dbscan(X, float(sys.argv[2]), int(sys.argv[3]))

    _, dimension = X.shape
    plot_dbscan(db)

if __name__ == '__main__':
    main()
