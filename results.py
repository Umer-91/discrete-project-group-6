"""Compute Z-scores, display the tables and save the grouped bar chart."""

from math import sqrt


def calculate_z_scores(observed, random_counts):
    if not random_counts:
        raise ValueError("At least one random network is required.")

    scores = []
    for class_index in range(len(observed)):
        values = [counts[class_index] for counts in random_counts]
        mean = sum(values) / len(values)
        variance = sum((value - mean) ** 2 for value in values) / len(values)
        standard_deviation = sqrt(variance)

        if standard_deviation == 0:
            scores.append(0.0)
        else:
            scores.append((observed[class_index] - mean) / standard_deviation)
    return scores


def label_score(score):
    if score > 2:
        return "motif"
    if score < -2:
        return "anti-motif"
    return "neither"


def print_results(dept_a, counts_a, scores_a, dept_b, counts_b, scores_b):
    print(f"\nA = department {dept_a}, B = department {dept_b}")
    print("Class  Count A  Count B      Z A      Z B   Result A     Result B")
    for i in range(13):
        print(
            f"{i + 1:>5}  {counts_a[i]:>7}  {counts_b[i]:>7}"
            f"  {scores_a[i]:>7.3f}  {scores_b[i]:>7.3f}"
            f"   {label_score(scores_a[i]):<11}  {label_score(scores_b[i])}"
        )


def save_chart(group_r, dept_a, scores_a, dept_b, scores_b, path):
    import matplotlib.pyplot as plt

    classes = list(range(1, 14))
    width = 0.36

    figure, axes = plt.subplots(figsize=(10, 5), layout="constrained")
    axes.bar([i - width / 2 for i in classes], scores_a, width,
             label=f"A · Department {dept_a}", color="#2855a6")
    axes.bar([i + width / 2 for i in classes], scores_b, width,
             label=f"B · Department {dept_b}", color="#c56323")
    axes.axhline(2, color="#444444", linestyle="--", linewidth=1)
    axes.axhline(-2, color="#444444", linestyle="--", linewidth=1)
    axes.axhline(0, color="#777777", linewidth=0.7)
    axes.set_xticks(classes)
    axes.set_xlabel("Triad class")
    axes.set_ylabel("Z-score")
    axes.set_title(f"Email triad Z-scores | R = {group_r}")
    axes.legend()
    figure.savefig(path, dpi=180)
    plt.close(figure)
