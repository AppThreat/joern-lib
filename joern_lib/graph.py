"""
Module to work with networkx graph data
"""
import json
import tempfile
from collections import Counter, defaultdict

import networkx as nx
from networkx.readwrite import json_graph, read_graphml

from joern_lib.utils import calculate_hash

try:
    import pydotplus
except ImportError:
    pass


def convert_dot(data):
    """
    Function to convert dot data into graph
    """
    if not data:
        return None
    graph_list = []
    data_list = data
    if isinstance(data, str):
        data_list = [data]
    for d in data_list:
        with tempfile.NamedTemporaryFile(prefix="graph", suffix=".dot") as fp:
            pydotplus.parser.parse_dot_data(d).write(fp.name)
            G = nx.Graph(nx.nx_agraph.read_dot(fp))
            graph_list.append(G)
    return graph_list[0] if len(graph_list) == 1 else graph_list


def _hash_label(label, digest_size):
    return calculate_hash(label, digest_size=digest_size)


def _init_node_labels(G, edge_attr_fn, node_attr_fn):
    if node_attr_fn:
        return {u: node_attr_fn(dd) for u, dd in G.nodes(data=True)}
    elif edge_attr_fn:
        return {u: "" for u in G}
    else:
        return {u: str(deg) for u, deg in G.degree()}


def _neighborhood_aggregate(G, node, node_labels, edge_attr_fn=None):
    """
    Compute new labels for given node by aggregating
    the labels of each node's neighbors.
    """
    label_list = []
    for nbr in G.neighbors(node):
        prefix = "" if edge_attr_fn is None else edge_attr_fn(G[node][nbr])
        label_list.append(prefix + node_labels[nbr])
    return node_labels[node] + "".join(sorted(label_list))


def graph_hash(G, edge_attr_fn=None, node_attr_fn=None, iterations=3, digest_size=16):
    """Return Weisfeiler Lehman (WL) graph hash"""

    def weisfeiler_lehman_step(G, labels, edge_attr_fn=None):
        """
        Apply neighborhood aggregation to each node
        in the graph.
        Computes a dictionary with labels for each node.
        """
        new_labels = {}
        for node in G.nodes():
            label = _neighborhood_aggregate(G, node, labels, edge_attr_fn=edge_attr_fn)
            new_labels[node] = _hash_label(label, digest_size)
        return new_labels

    # set initial node labels
    node_labels = _init_node_labels(G, edge_attr_fn, node_attr_fn)

    subgraph_hash_counts = []
    for _ in range(iterations):
        node_labels = weisfeiler_lehman_step(G, node_labels, edge_attr_fn=edge_attr_fn)
        counter = Counter(node_labels.values())
        # sort the counter, extend total counts
        subgraph_hash_counts.extend(sorted(counter.items(), key=lambda x: x[0]))

    # hash the final counter
    return _hash_label(str(tuple(subgraph_hash_counts)), digest_size)


def subgraph_hashes(
    G, edge_attr_fn=None, node_attr_fn=None, iterations=3, digest_size=16
):
    """Return a dictionary of subgraph hashes by node."""

    def weisfeiler_lehman_step(G, labels, node_subgraph_hashes, edge_attr_fn=None):
        """
        Apply neighborhood aggregation to each node
        in the graph.
        Computes a dictionary with labels for each node.
        Appends the new hashed label to the dictionary of subgraph hashes
        originating from and indexed by each node in G
        """
        new_labels = {}
        for node in G.nodes():
            label = _neighborhood_aggregate(G, node, labels, edge_attr_fn=edge_attr_fn)
            hashed_label = _hash_label(label, digest_size)
            new_labels[node] = hashed_label
            node_subgraph_hashes[node].append(hashed_label)
        return new_labels

    node_labels = _init_node_labels(G, edge_attr_fn, node_attr_fn)

    node_subgraph_hashes = defaultdict(list)
    for _ in range(iterations):
        node_labels = weisfeiler_lehman_step(
            G, node_labels, node_subgraph_hashes, edge_attr_fn
        )

    return dict(node_subgraph_hashes)


def diff(first_graph, second_graph, include_common=False, as_dict=False, as_dot=False):
    """Function to compute the difference between two graphs"""
    return diff_graph(
        first_graph,
        second_graph,
        include_common=include_common,
        as_dict=as_dict,
        as_dot=as_dot,
    )


def get_node_label(n):
    """Retrieve a label for the node from various data attributes"""
    if not n:
        return ""
    for at in (
        "label",
        "CODE",
        "SIGNATURE",
        "METHOD_FULL_NAME",
        "NAME",
        "VARIABLE",
        "labelE",
    ):
        if n.get(at) is not None:
            return n.get(at)
    return ""


def diff_graph(
    first_graph, second_graph, include_common=False, as_dict=False, as_dot=False
):
    """Function to compute the difference between two graphs and optionally convert the result to dict or dot format"""
    if not first_graph and second_graph:
        return second_graph
    if first_graph and not second_graph:
        return first_graph
    graph = nx.Graph()
    if not first_graph and not second_graph:
        return graph
    first_graph_nodes = [get_node_label(r[1]) for r in first_graph.nodes(data=True)]
    second_graph_nodes = [get_node_label(r[1]) for r in second_graph.nodes(data=True)]
    removed_nodes = set(first_graph_nodes) - set(second_graph_nodes)
    added_nodes = set(second_graph_nodes) - set(first_graph_nodes)
    nodes = set(second_graph_nodes) & set(first_graph_nodes)
    first_graph_edges = [
        (r[0], r[1], get_node_label(r[2])) for r in first_graph.edges(data=True)
    ]
    second_graph_edges = [
        (r[0], r[1], get_node_label(r[2])) for r in second_graph.edges(data=True)
    ]
    removed_edges = set(first_graph_edges) - set(second_graph_edges)
    removed_edges_fmt = []
    for removed_edge in removed_edges:
        src = removed_edge[0]
        dest = removed_edge[1]
        if removed_edge[0] in removed_nodes:
            src = "-" + removed_edge[0]
        if removed_edge[1] in removed_nodes:
            dest = "-" + removed_edge[1]
        removed_edges_fmt.append((src, dest, removed_edge[2]))
    added_edges = set(second_graph_edges) - set(first_graph_edges)
    added_edges_fmt = []
    for added_edge in added_edges:
        src = added_edge[0]
        dest = added_edge[1]
        if added_edge[0] in added_nodes:
            src = "+" + added_edge[0]
        if added_edge[1] in added_nodes:
            dest = "+" + added_edge[1]
        added_edges_fmt.append((src, dest, added_edge[2]))
    edges = set(second_graph_edges) & set(first_graph_edges)
    for removed_node in removed_nodes:
        graph.add_node("-" + removed_node)
    for added_node in added_nodes:
        graph.add_node("+" + added_node)
    if include_common:
        for node in nodes:
            graph.add_node(node)
    for removed_edge in removed_edges_fmt:
        graph.add_edge(removed_edge[0], removed_edge[1], label="-" + removed_edge[2])
    for added_edge in added_edges_fmt:
        graph.add_edge(added_edge[0], added_edge[1], label="+" + added_edge[2])
    if include_common:
        for edge in edges:
            graph.add_edge(edge[0], edge[1], label=edge[2])
    if as_dict:
        return nx.to_dict_of_dicts(graph)
    if as_dot:
        with tempfile.NamedTemporaryFile(
            prefix="diff_graph", suffix=".dot", delete=False
        ) as fp:
            write_dot(graph, fp.name)
            fp.flush()
            return fp.read().decode()
    return graph


def node_match_fn(n1, n2):
    return get_node_label(n1) == get_node_label(n2)


def gep(first_graph, second_graph, upper_bound=500):
    """Function to compute the difference based on optimal edit path algorithm"""
    return nx.optimal_edit_paths(
        first_graph,
        second_graph,
        node_match=node_match_fn,
        edge_match=node_match_fn,
        upper_bound=upper_bound,
    )


def ged(first_graph, second_graph, timeout=5, upper_bound=500):
    """Function to compute the difference based on graph edit distance algorithm"""
    return nx.graph_edit_distance(
        first_graph,
        second_graph,
        node_match=node_match_fn,
        edge_match=node_match_fn,
        timeout=timeout,
        upper_bound=upper_bound,
    )


def write_dot(G, path):
    """Function to export graph as dot"""
    nx.nx_agraph.write_dot(G, path)


def hash(
    G,
    subgraph=False,
    edge_attr_fn=get_node_label,
    node_attr_fn=get_node_label,
    iterations=3,
    digest_size=16,
):
    """Function to compute the hashes for a graph using Weisfeiler Lehman hashing algorithm"""
    if subgraph:
        return subgraph_hashes(
            G,
            edge_attr_fn=edge_attr_fn,
            node_attr_fn=node_attr_fn,
            iterations=iterations,
            digest_size=digest_size,
        )
    return graph_hash(
        G,
        edge_attr_fn=edge_attr_fn,
        node_attr_fn=node_attr_fn,
        iterations=iterations,
        digest_size=digest_size,
    )


def summarize(G, as_dict=False, as_dot=False):
    """Function to summarize the graph based on node labels"""
    summary_graph = nx.snap_aggregation(
        G, node_attributes=("label", "CODE"), edge_attributes=("label", "CODE")
    )
    if as_dict:
        return nx.to_dict_of_dicts(summary_graph)
    if as_dot:
        with tempfile.NamedTemporaryFile(
            prefix="summary_graph", suffix=".dot", delete=False
        ) as fp:
            write_dot(summary_graph, fp.name)
            fp.flush()
            return fp.read().decode()
    return summary_graph


def is_similar(M1, M2, upper_bound=500, timeout=5):
    """Function to check if two graphs are similar. To simplify the problem, first the raw graph difference is computed to check if the graphs are the same.
    If not graph edit distance is computed with a fixed timeout to help answer the question
    """
    if not diff_graph(M1, M2, as_dict=True):
        return True
    distance = ged(M1, M2, upper_bound=upper_bound, timeout=timeout)
    if distance is None:
        return False
    return True


def convert_graphml(
    gml_file, force_multigraph=False, as_graph=True, as_adjacency_data=False
):
    """Function to convert graphml to networkx"""
    try:
        G = read_graphml(gml_file, force_multigraph=force_multigraph)
        if as_graph:
            return G
        if as_adjacency_data:
            return json.dumps(json_graph.adjacency_data(G))
    except Exception:
        return None
