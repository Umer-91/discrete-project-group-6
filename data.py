

import gzip
from itertools import combinations
from pathlib import Path
from urllib.request import urlretrieve

DATA_FOLDER = Path(__file__).resolve().parent / "data"
EDGES_FILE = "email-Eu-core.txt.gz"
LABELS_FILE = "email-Eu-core-department-labels.txt.gz"
SNAP_URL = "https://snap.stanford.edu/data/"


def download_data(folder):
    folder.mkdir(parents=True, exist_ok=True)
    for filename in (EDGES_FILE, LABELS_FILE):
        path = folder / filename
        if not path.exists():
            print(f"Downloading {filename}...")
            temporary_path = path.with_suffix(".part")
            urlretrieve(SNAP_URL + filename, temporary_path)
            temporary_path.replace(path)


def read_pairs(path):
    with gzip.open(path, "rt", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):
                first, second = line.split()
                yield int(first), int(second)


def load_data(folder):
    departments = dict(read_pairs(folder / LABELS_FILE))
    edges = set()

    for sender, receiver in read_pairs(folder / EDGES_FILE):
        if sender != receiver:
            edges.add((sender, receiver))

    return departments, edges


def rank_departments(departments, edges):
    internal_counts = dict.fromkeys(departments.values(), 0)
    for sender, receiver in edges:
        department = departments[sender]
        if department == departments[receiver]:
            internal_counts[department] += 1

    ranked = sorted(internal_counts, key=lambda d: (-internal_counts[d], d))
    return ranked[:20], internal_counts


def select_departments(top_twenty, group_r):
    pairs = list(combinations(range(20), 2))
    first_index, second_index = pairs[group_r % len(pairs)]
    return first_index, second_index, top_twenty[first_index], top_twenty[second_index]


def department_graph(department, departments, edges):
    members = {node for node, label in departments.items() if label == department}
    internal_edges = {
        (sender, receiver)
        for sender, receiver in edges
        if sender in members and receiver in members
    }
    return members, internal_edges
