"""Draw the two department graphs as labelled nodes and directed arrows."""

from math import cos, sin, tau

import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from matplotlib.patches import FancyArrowPatch

from data import DATA_FOLDER, department_graph, load_data, rank_departments, select_departments
from main import GROUP_R


def draw_network(department, nodes, edges):
    positions = {}
    for index, node in enumerate(sorted(nodes)):
        angle = tau / 4 - tau * index / len(nodes)
        positions[node] = (cos(angle), sin(angle))

    figure, axes = plt.subplots(figsize=(12, 12))
    figure.subplots_adjust(left=0.05, right=0.95, bottom=0.06, top=0.90)
    # Curving both directions puts reciprocal arrows on opposite sides.
    line_opacity = 0.23 if len(edges) > 300 else 0.45
    for sender, receiver in sorted(edges):
        curve = 0.10 if (receiver, sender) in edges else 0
        arrow = FancyArrowPatch(
            positions[sender], positions[receiver],
            connectionstyle=f"arc3,rad={curve}",
            arrowstyle="-|>", mutation_scale=9, shrinkA=6, shrinkB=6,
            edgecolor=to_rgba("#284666", line_opacity),
            facecolor=to_rgba("#284666", 0.72), linewidth=0.7,
        )
        axes.add_patch(arrow)

    for node, (x, y) in positions.items():
        axes.scatter(x, y, s=105, facecolor="#cfe2ff", edgecolor="#214a71", zorder=3)
        axes.text(1.065 * x, 1.065 * y, str(node),
                  ha="center", va="center", fontsize=9, color="#172f49")

    axes.set(xlim=(-1.14, 1.14), ylim=(-1.14, 1.14), aspect="equal")
    axes.set_axis_off()
    figure.suptitle(f"Department {department} email network | R = {GROUP_R}",
                    y=0.96, fontsize=22, fontweight="bold")
    figure.text(0.5, 0.92, f"{len(nodes)} people · {len(edges)} directed email links",
                ha="center", fontsize=14)
    figure.text(0.5, 0.047, "Labels are person IDs. Arrows point from sender to receiver.",
                ha="center", fontsize=12)
    path = f"department_{department}_network.png"
    figure.savefig(path, dpi=200)
    plt.close(figure)
    print(f"Saved {path} ({len(nodes)} nodes, {len(edges)} edges)")


def main():
    departments, edges = load_data(DATA_FOLDER)
    top_twenty, _ = rank_departments(departments, edges)
    _, _, department_a, department_b = select_departments(top_twenty, GROUP_R)
    for department in (department_a, department_b):
        nodes, internal_edges = department_graph(department, departments, edges)
        draw_network(department, nodes, internal_edges)


if __name__ == "__main__":
    main()
