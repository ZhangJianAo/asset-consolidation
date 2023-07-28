import numpy as np
from numpy.linalg import norm

ASSETS = [
    {
        'ips': ['10.33.70.221'],
        'macs': ['00:50:56:a8:ea:02'],
        'hostname': ['dev-secker'],
        'sn': ['VMware-42287c442ae0cd86-06e9a9d4976d2cf3']
    },
    {
        'ips': ['10.33.70.218'],
        'macs': ['00:50:56:a8:b6:7f'],
        'hostname': ['test-secker-server'],
        'sn': ['VMware-4228cd2f9a22f4f3-1a8ac867e27b4dd6']
    },
    {
        'ips': ['10.20.0.21', 'fe80::44e:458f:d83d:33e6'],
        'macs': ['38:f9:d3:8d:6d:33'],
        'hostname': ['my-macbookpro'],
        'sn': ['D02Y801AXRJ5']
    },
    # testing asset
    {
        'ips': ['fe80::44e:458f:d83d:33e6'],
        'hostname': ['my-macbookpro']
    },
    {
        'ips': ['10.20.0.21']
    },
    {
        'ips': ['127.0.0.1'],
        'macs': ['00:50:56:a8:b6:7f']
    },
    {
        'ips': ['10.33.70.218'],
        'macs': ['38:f9:d3:8d:6d:33'],
        'sn': ['D02Y801AXRJ5']
    }
]


def create_bag(asset):
    bag = set()
    for k, v in asset.items():
        if k in ('ips', 'macs', 'hostname', 'sn'):
            bag.update(v)
    return bag


ASSET_BAGS = [create_bag(a) for a in ASSETS]


def one_hot_encodes():
    kw = {}
    idx = 0

    all_keys = set().union(*ASSET_BAGS)

    for k in all_keys:
        kw[k] = idx
        idx += 1

    def gen_vector(kwset):
        result = [0] * idx
        for k in kwset:
            ki = kw[k]
            result[ki] = 1
        return result

    return [gen_vector(bag) for bag in ASSET_BAGS]


def cosine_similarity(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))


def jaccard_similarity(a, b):
    total = 0
    inter = 0
    for i in range(0, len(a)):
        if a[i] == 1 or b[i] == 1:
            total += 1
        if a[i] == 1 and b[i] == 1:
            inter += 1
    return inter / total


def one_hot_vector_jaccard(a, b):
    total = 0
    inter = 0
    for i in range(0, len(a)):
        if a[i] == 1 or b[i] == 1:
            total += 1
        if a[i] == 1 and b[i] == 1:
            inter += 1
    return inter / total
