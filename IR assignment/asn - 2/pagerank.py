import networkx as nx

# Create a directed graph of web pages
web = nx.DiGraph()

# Add links between pages
web.add_edges_from([
    ("A", "B"),
    ("A", "C"),
    ("B", "C"),
    ("C", "A"),
    ("D", "C")
])

# Calculate PageRank scores
rank = nx.pagerank(
    web,
    alpha=0.85,
    max_iter=100
)

# Display the results
print("===== PAGERANK RESULTS =====")

for page, score in sorted(rank.items()):
    print(f"Page {page}: {score:.4f}")

# Display pages from highest to lowest rank
print("\n===== RANKED WEB PAGES =====")

for page, score in sorted(
    rank.items(),
    key=lambda item: item[1],
    reverse=True
):
    print(f"Page {page}: {score:.4f}")