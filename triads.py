

from itertools import combinations, permutations

EDGE_ORDER = ((0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1))
CANONICAL_CODES = (3, 6, 7, 10, 11, 15, 21, 23, 25, 27, 30, 31, 63)
CLASS_BY_CODE = {code: number for number, code in enumerate(CANONICAL_CODES, 1)}


def canonical_code(mask):
    present_edges = set()
    for bit, edge in enumerate(EDGE_ORDER):
        if mask & (1 << bit):
            present_edges.add(edge)

    best_code = mask
    for order in permutations(range(3)):
        code = encode_edges(order, present_edges)
        best_code = min(best_code, code)
    return best_code


def encode_edges(nodes, edges):
    code = 0
    for bit, (source, target) in enumerate(EDGE_ORDER):
        if (nodes[source], nodes[target]) in edges:
            code |= 1 << bit
    return code


# Every possible six-bit mask gets classified once at startup.
CLASS_BY_MASK = [
    CLASS_BY_CODE.get(canonical_code(mask), 0)
    for mask in range(64)
]


def triad_class(a, b, c, edges):
    """Return 1–13 for a connected triad, or 0 for a disconnected triple."""
    code = encode_edges((a, b, c), edges)
    return CLASS_BY_MASK[code]


def count_triads(nodes, edges):
    neighbours = {node: set() for node in nodes}
    for sender, receiver in edges:
        neighbours[sender].add(receiver)
        neighbours[receiver].add(sender)

    counts = [0] * 13
    for centre in nodes:
        for first, second in combinations(neighbours[centre], 2):
            # A triangle has three possible centres. Count it at its smallest ID.
            if second in neighbours[first] and centre != min(centre, first, second):
                continue

            class_number = triad_class(centre, first, second, edges)
            counts[class_number - 1] += 1
    return counts
