import xml.etree.ElementTree as ET
import networkx as nx
import matplotlib.pyplot as plt


def parse_xml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    pages = {}

    # Extract page information from XML
    for page in root.findall("page"):
        page_id = page.get("id")
        topic = page.get("topic", "Unknown")

        title_element = page.find("title")
        title = (
            title_element.text.strip()
            if title_element is not None and title_element.text
            else page_id
        )

        links = [
            link.text.strip()
            for link in page.findall("link")
            if link.text and link.text.strip()
        ]

        pages[page_id] = {
            "title": title,
            "topic": topic,
            "links": links
        }

    return pages


def generate_graph(pages):
    graph = nx.DiGraph()

    # Add pages as nodes
    for page_id, info in pages.items():
        graph.add_node(
            page_id,
            title=info["title"],
            topic=info["topic"]
        )

    # Add hyperlinks as directed edges
    for page_id, info in pages.items():
        for target in info["links"]:
            if target in pages:
                graph.add_edge(page_id, target)

    return graph


def topic_specific_pagerank(graph, pages, topic):
    # Give preference to pages matching the chosen topic
    relevant_pages = [
        page_id
        for page_id, info in pages.items()
        if info["topic"].lower() == topic.lower()
    ]

    if not relevant_pages:
        print("No pages found for topic:", topic)
        return {}

    # Personalization values must sum to 1
    personalization = {
        page_id: (
            1 / len(relevant_pages)
            if page_id in relevant_pages else 0
        )
        for page_id in graph.nodes()
    }

    scores = nx.pagerank(
        graph,
        alpha=0.85,
        personalization=personalization
    )

    return scores


def main():
    pages = parse_xml("web_data.xml")
    graph = generate_graph(pages)

    print("===== WEB GRAPH =====")
    print("Number of pages:", graph.number_of_nodes())
    print("Number of links:", graph.number_of_edges())
    print("Links:", list(graph.edges()))

    topic = input(
        "\nEnter topic (AI, Python, Database): "
    ).strip()

    scores = topic_specific_pagerank(
        graph, pages, topic
    )

    if not scores:
        return

    print("\n===== TOPIC-SPECIFIC PAGERANK =====")

    ranked_pages = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    for page_id, score in ranked_pages:
        print(
            f"{page_id} - {pages[page_id]['title']} "
            f"({pages[page_id]['topic']}): {score:.4f}"
        )

    # Visualize the graph
    colors = [
        "lightgreen"
        if pages[node]["topic"].lower() == topic.lower()
        else "skyblue"
        for node in graph.nodes()
    ]

    positions = nx.spring_layout(graph, seed=42)

    nx.draw(
        graph,
        positions,
        with_labels=True,
        node_color=colors,
        node_size=2200,
        font_weight="bold",
        arrows=True
    )

    plt.title("Topic-Specific Web Graph: " + topic)
    plt.show()


if __name__ == "__main__":
    main()