from sklearn.cluster import AgglomerativeClustering, DBSCAN, HDBSCAN, OPTICS, Birch, AffinityPropagation, MeanShift
import numpy as np
import asset_data


np.set_printoptions(suppress=True)
one_hot_vectors = asset_data.one_hot_encodes()
dist_matirx = np.array(
    [
        [1-asset_data.jaccard_similarity(x, y) for y in one_hot_vectors] for x in one_hot_vectors
    ], np.float32)
print(dist_matirx)


def print_cluster(result):
    print(result.__class__.__name__, ":", result.labels_)


print_cluster(
    AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=0.7,
        linkage='single',
        metric='precomputed',
        compute_distances=True
    ).fit(dist_matirx)
)
print_cluster(
    DBSCAN(eps=1, min_samples=2).fit(dist_matirx)
)
print_cluster(
    HDBSCAN(min_cluster_size=2).fit(dist_matirx)
)
print_cluster(
    OPTICS(min_samples=2).fit(dist_matirx)
)
print_cluster(
    Birch(n_clusters=None).fit(dist_matirx)
)
print_cluster(
    AffinityPropagation().fit(dist_matirx)
)
print_cluster(
    MeanShift().fit(dist_matirx)
)
