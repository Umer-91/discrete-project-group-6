
Finding Network Motifs in an Email Network
Discrete Structures - Fall 2026
Group 6

Group members

Umer Asif - 25i-0733
Muhammad Maaz - 25i-0735
Arqum Mehtab - 25i-0896
Farhan Ali - 25i-0724

About the project

This project looks at email connections inside two departments using the SNAP email-Eu-core dataset. Each person is a node, and an arrow means one person emailed another. The program counts the 13 connected patterns that can appear between three people. It then compares those counts with randomized graphs to find motifs and anti-motifs.

Our settings

R = 733 + 735 + 896 + 724 = 3088
Pair number = 3088 mod 190 = 48
Positions in the top-20 department list = (2, 14), counting from zero
Department A = 7, with 51 nodes and 679 edges
Department B = 5, with 18 nodes and 147 edges
Random graphs per department = 20 + (3088 mod 31) = 39
Swap attempts per edge = 5 + (3088 mod 6) = 9
Attempts per random graph = 6111 for A and 1323 for B
Base random seed = 3088

Departments are ranked by their number of internal edges, from largest to smallest. Ties are broken by the smaller department ID.

How to run

Install Python 3. Open a terminal in the folder containing main.py and run these commands in order.

python -m pip install matplotlib
python main.py --download

The second command downloads the dataset into a local data folder and runs the analysis. Once the data is there, you can run it again with this command.

python main.py

The program prints the settings, both departments' triad counts and Z-scores. It also saves the chart as motifs_R3088.png.

To print the actual node IDs and edges, run this command.

python main.py --parameters-only --show-graph

What the files do

main.py runs the project and sets the group parameters.
data.py loads and cleans the data and selects the departments.
triads.py classifies and counts the connected triads.
null_model.py randomizes the edges and checks that degrees stay the same.
results.py calculates Z-scores and creates the chart.
motifs_R3088.png shows the Z-scores for both departments.

How the method works

Self-loops and repeated edges are removed first. For each department, the program keeps all its members and the edges between them. Connected triples are found through pairs of neighbours and counted once. Each triple is classified by checking all six node orderings and choosing the smallest six-bit code.

Each random graph starts from the original department graph. Two edges exchange their receivers. Swaps that create self-loops or repeated edges are rejected, and rejected attempts still count. Assertions check that every person's incoming and outgoing degrees stay the same.

For each class, Z is the observed count minus the random mean, divided by the population standard deviation. If the standard deviation is zero, Z is reported as zero. A score above 2 is a motif, and a score below -2 is an anti-motif.

Example by hand

Suppose the only edges between people 5, 7 and 9 are 5 -> 7 and 5 -> 9. The six possible edge positions have values 1, 2, 4, 8, 16 and 32, in the order 0 -> 1, 0 -> 2, 1 -> 0, 1 -> 2, 2 -> 0 and 2 -> 1.

Ordering (5, 7, 9) gives 1 + 2 = 3.
Ordering (5, 9, 7) gives 1 + 2 = 3.
Ordering (7, 5, 9) gives 4 + 8 = 12.
Ordering (7, 9, 5) gives 16 + 32 = 48.
Ordering (9, 5, 7) gives 4 + 8 = 12.
Ordering (9, 7, 5) gives 16 + 32 = 48.

The smallest code is 3, so this is Class 1.

Results

Department 7 has more two-way links within triples than its random baseline predicts. Its strongest motifs are Class 8 with Z = 8.540 and Class 13 with Z = 8.123. Class 8 has one person exchanging emails both ways with two people who have no link between them. In Class 13, every pair exchanges emails both ways. Class 3 also qualifies at Z = 2.002. Department 5's only motif in this run is Class 11 with Z = 2.296, where one person emails two people who exchange emails with each other. Class 1 is an anti-motif in both departments. Overall, mutual communication stands out more strongly in Department 7 relative to its own baseline. These results describe the presence of email connections. Message totals are unavailable in this dataset.

Contributions


Umer Asif handled data loading, group settings, the main program and README.
Muhammad Maaz handled triad classification and counting.
Arqum Mehtab handled randomization and degree checks.
Farhan Ali handled Z-scores, the chart and the results explanation.


Sources

SNAP email-Eu-core dataset
https://snap.stanford.edu/data/email-Eu-core.html

Milo et al. (2002), Network Motifs, Science 298, 824-827
https://doi.org/10.1126/science.298.5594.824
