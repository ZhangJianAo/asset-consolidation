# Asset Grouping

When building a system to discover asset from multiple data source,
a core challenge is to find identical asset data across different data sources and grouping them together.

https://www.axonius.com/blog/asset-inventory-correlation-problem

This project introduce a method to find identical assets and test is effect.

## Define

For example, if we have the following asset data:

    {'ips': ['10.33.70.221'], 'macs': ['00:50:56:a8:ea:02'], 'hostname': ['dev-secker'], 'sn': ['VMware-42287c442ae0cd86-06e9a9d4976d2cf3']},
    {'ips': ['10.33.70.218'], 'macs': ['00:50:56:a8:b6:7f'], 'hostname': ['test-secker-server'], 'sn': ['VMware-4228cd2f9a22f4f3-1a8ac867e27b4dd6']},
    {'ips': ['10.20.0.21', 'fe80::44e:458f:d83d:33e6'], 'macs': ['38:f9:d3:8d:6d:33'], 'hostname': ['my-macbookpro'], 'sn': ['D02Y801AXRJ5']},
    {'ips': ['fe80::44e:458f:d83d:33e6'], 'hostname': ['my-macbookpro']},
    {'ips': ['10.20.0.21']},
    {'ips': ['127.0.0.1'], 'macs': ['00:50:56:a8:b6:7f']},
    {'ips': ['10.33.70.218'], 'macs': ['38:f9:d3:8d:6d:33'], 'sn': ['D02Y801AXRJ5']}

The first 3 record are different asset.
The 4th record has the same ip and hostname with third record.
The 5th record has same ip address with third record.
The 6th record has same mac address with second record and has a wrong ip address.
The 7th record has same ip with second record and same mac and sn with third record, so it consider same asset with third record.

## Algorithm

### Vector Model

Consider encode each record to a vector, and calculate vector distance in the vector space.

### One-Hot Encoding

https://www.kaggle.com/code/dansbecker/using-categorical-data-with-one-hot-encoding/notebook

Using one-hot encoding method, treat every value of ip/mac/hostname/sn as a category,
if a record has this value, it is belongs to this category.

Function `one_hot_encodes` in `asset_data.py` file return encoded vector for each record.

### Vector Distance

To find how similar two records are, we need calculate vector's distance.

One method is calculated the two vectors cosine, another method is jaccard index.

Both algorithm can be calculated with only two records information, no need to consider all other records.

For example using One-Hot Encoding, if whole dataset has 10 unique values, the vector length will be 10.
When calculate two records distance, if these two records has only 3 unique values, like:

    r1: [1, 0, 1, 0, 0, 0, 0, 0, 0, 0]
    r2: [1, 1, 0, 0, 0, 0, 0, 0, 0, 0]

Their distance are equal to following vectors distance:

    r1: [1, 0, 1]
    r2: [1, 1, 0]

### Clustering

Using clustering algorithm can find the similar records and group them together.

## Testing Results

### Cosine Similarity

Distance between records are:

    [[ 0.     1.     1.     1.     1.     1.     1.   ]
     [ 1.     0.     1.     1.     1.     0.646  0.711]
     [ 1.     1.     0.     0.367  0.552  1.     0.483]
     [ 1.     1.     0.367  0.     1.     1.     1.   ]
     [ 1.     1.     0.552  1.     0.     1.     1.   ]
     [ 1.     0.646  1.     1.     1.     0.     1.   ]
     [ 1.     0.711  0.483  1.     1.     1.     -0.  ]]

Each row in matrix means a record distance between each other record.

Distance is present from 0 to 1, 0 means same, 1 means no relevant.

First row shows the first record, it is same with itself, so first item is 0,
and the first record has no relevant with all other record, so the rest items are 1.

Result of different clustering algorithm:

    AgglomerativeClustering : [1 0 2 2 2 0 2]
    DBSCAN : [-1  0  1  1 -1  0 -1]
    HDBSCAN : [-1  0  1  1  1  0  1]
    OPTICS : [-1  0  1  1  1  0  1]
    Birch : [0 1 2 2 3 1 4]
    AffinityPropagation : [0 1 2 2 2 1 2]
    MeanShift : [4 1 0 0 2 1 3]

The array of clustering algorithm showing the group number for each record.

For example `[1 0 2 2 2 0 2]` means first record in group 1, second and sixth record in group 0, other records in group 2.

Number `-1` means this record not belong to any group.

Grouping second and sixth records together is correct, grouping third, 4th, 5th records together is correct.

The 7th record are tricky, it's better grouping it with third record.

The result shows the AgglomerativeClustering, HDBSCAN, OPTICS and AffinityPropagation algorithms output best result.

The `AgglomerativeClustering` need to set `distance_threshold` to 0.7 to get best result.

The `DBSCAN` and `HDBSCAN` need to set `min_cluster_size` to 2 and `OPTICS` need to set `min_samples` to 2.

### Jaccard Similarity

Distance between records are:

    [[0.     1.     1.     1.     1.     1.     1.   ]
     [1.     0.     1.     1.     1.     0.8    0.833]
     [1.     1.     0.     0.6    0.8    1.     0.666]
     [1.     1.     0.6    0.     1.     1.     1.   ]
     [1.     1.     0.8    1.     0.     1.     1.   ]
     [1.     0.8    1.     1.     1.     0.     1.   ]
     [1.     0.833  0.666  1.     1.     1.     0.   ]]

Result of different clustering algorithm:

    AgglomerativeClustering : [3 4 0 0 1 2 0]
    DBSCAN : [-1 -1  0  0 -1 -1 -1]
    HDBSCAN : [-1  1  0  0 -1  1  0]
    OPTICS : [-1  1  0  0 -1  1  0]
    Birch : [0 1 2 2 3 4 5]
    AffinityPropagation : [0 2 1 1 1 2 1]
    MeanShift : [4 3 0 0 1 2 0]

Most algorithm's result is not as good as cosine similarity, except `AffinityPropagation`.

Looks cosine similarity values are more smoothly than the jaccard similarity.

## Conclusion

`Cosine Similarity` is better.

`AffinityPropagation` has best result in each similarity algorithm.

`HDBSCAN` and `OPTICS` are also good.