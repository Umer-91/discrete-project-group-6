

import argparse
from pathlib import Path
import random

from data import DATA_FOLDER, department_graph, download_data, load_data
from data import rank_departments, select_departments
from null_model import randomize
from results import calculate_z_scores, print_results, save_chart
from triads import count_triads

GROUP_R = 733 + 735 + 896 + 724
RANDOM_NETWORKS = 20 + GROUP_R % 31
ATTEMPTS_PER_EDGE = 5 + GROUP_R % 6


def analyse_department(nodes, edges, seeds):
    attempts = ATTEMPTS_PER_EDGE * len(edges)
    observed = count_triads(nodes, edges)
    random_counts = []

    for seed in seeds:
        random_edges = randomize(edges, attempts, seed)
        random_counts.append(count_triads(nodes, random_edges))

    return observed, calculate_z_scores(observed, random_counts)


def print_graph(label, department, nodes, edges, show_graph):
    print(
        f"{label}: department {department}, {len(nodes)} nodes, "
        f"{len(edges)} edges, {ATTEMPTS_PER_EDGE * len(edges)} swap attempts per network"
    )
    if show_graph:
        print(f"Nodes: {sorted(nodes)}")
        print(f"Edges: {sorted(edges)}")


def main():
    parser = argparse.ArgumentParser(description="Compare two SNAP email departments.")
    parser.add_argument("--data-dir", type=Path, default=DATA_FOLDER)
    parser.add_argument("--download", action="store_true", help="Download the two SNAP files")
    parser.add_argument("--parameters-only", action="store_true", help="Print T1 and T2")
    parser.add_argument("--show-graph", action="store_true", help="List the actual nodes and edges")
    parser.add_argument("--chart", type=Path, default=Path("motifs_R3088.png"))
    args = parser.parse_args()

    try:
        if args.download:
            download_data(args.data_dir)
        departments, edges = load_data(args.data_dir)
    except OSError as error:
        parser.exit(1, f"Could not load SNAP data. Check data/ or use --download.\n{error}\n")

    top_twenty, internal_counts = rank_departments(departments, edges)
    index_a, index_b, dept_a, dept_b = select_departments(top_twenty, GROUP_R)
    nodes_a, edges_a = department_graph(dept_a, departments, edges)
    nodes_b, edges_b = department_graph(dept_b, departments, edges)

    print(f"R = {GROUP_R}")
    print(f"Top 20 (department, internal edges): {[(d, internal_counts[d]) for d in top_twenty]}")
    print(f"Pair index: {GROUP_R % 190}, positions: ({index_a}, {index_b})")
    print(f"Random networks per department: {RANDOM_NETWORKS}")
    print(f"Attempts per edge: {ATTEMPTS_PER_EDGE}, base seed: {GROUP_R}")
    print_graph("A", dept_a, nodes_a, edges_a, args.show_graph)
    print_graph("B", dept_b, nodes_b, edges_b, args.show_graph)

    if args.parameters_only:
        return

    # One generator seeded with R supplies a fresh seed for every random graph.
    rng = random.Random(GROUP_R)
    seeds_a = [rng.getrandbits(64) for _ in range(RANDOM_NETWORKS)]
    seeds_b = [rng.getrandbits(64) for _ in range(RANDOM_NETWORKS)]
    counts_a, scores_a = analyse_department(nodes_a, edges_a, seeds_a)
    counts_b, scores_b = analyse_department(nodes_b, edges_b, seeds_b)

    print_results(dept_a, counts_a, scores_a, dept_b, counts_b, scores_b)
    save_chart(GROUP_R, dept_a, scores_a, dept_b, scores_b, args.chart)
    print(f"Saved chart to {args.chart}")


if __name__ == "__main__":
    main()
