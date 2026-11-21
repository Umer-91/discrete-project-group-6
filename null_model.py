

import random
from collections import Counter


def degrees(edges):
    out_degree = Counter()
    in_degree = Counter()
    for sender, receiver in edges:
        out_degree[sender] += 1
        in_degree[receiver] += 1
    return out_degree, in_degree


def randomize(edges, attempts, seed):
    rng = random.Random(seed)
    edge_list = sorted(edges)
    edge_set = set(edge_list)

    if len(edge_list) >= 2:
        positions = range(len(edge_list))

        for _ in range(attempts):
            first, second = rng.sample(positions, 2)
            a, b = edge_list[first]
            c, d = edge_list[second]

            new_first = (a, d)
            new_second = (c, b)
            if a == d or c == b or new_first in edge_set or new_second in edge_set:
                continue

            edge_set.remove((a, b))
            edge_set.remove((c, d))
            edge_set.add(new_first)
            edge_set.add(new_second)

            edge_list[first] = new_first
            edge_list[second] = new_second

    assert degrees(edge_set) == degrees(edges), "A swap changed a node's degree"
    assert len(edge_set) == len(edges), "A swap changed the number of edges"
    assert all(sender != receiver for sender, receiver in edge_set)
    return edge_set
