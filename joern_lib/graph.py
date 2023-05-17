import tempfile

import networkx as nx

try:
    import pydotplus
except ImportError:
    pass


def convert_dot(data):
    """
    Method to convert dot data into graph
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


def diff(first_graph, second_graph, include_common=False, as_dict=False, as_dot=False):
    return diff_graph(
        first_graph,
        second_graph,
        include_common=include_common,
        as_dict=as_dict,
        as_dot=as_dot,
    )


def diff_graph(
    first_graph, second_graph, include_common=False, as_dict=False, as_dot=False
):
    first_graph_nodes = [r[1]["label"] for r in first_graph.nodes(data=True)]
    second_graph_nodes = [r[1]["label"] for r in second_graph.nodes(data=True)]
    removed_nodes = set(first_graph_nodes) - set(second_graph_nodes)
    added_nodes = set(second_graph_nodes) - set(first_graph_nodes)
    nodes = set(second_graph_nodes) & set(first_graph_nodes)
    first_graph_edges = [
        (r[0], r[1], r[2]["label"]) for r in first_graph.edges(data=True)
    ]
    second_graph_edges = [
        (r[0], r[1], r[2]["label"]) for r in second_graph.edges(data=True)
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
    graph = nx.Graph()
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
    return n1.get("label") == n2.get("label")


def gep(first_graph, second_graph, upper_bound=500):
    return nx.optimal_edit_paths(
        first_graph,
        second_graph,
        node_match=node_match_fn,
        edge_match=node_match_fn,
        upper_bound=upper_bound,
    )


def ged(first_graph, second_graph, timeout=5, upper_bound=500):
    return nx.graph_edit_distance(
        first_graph,
        second_graph,
        node_match=node_match_fn,
        edge_match=node_match_fn,
        timeout=timeout,
        upper_bound=upper_bound,
    )


def write_dot(G, path):
    nx.nx_agraph.write_dot(G, path)


def hash(
    G,
    subgraph=False,
    edge_attr="label",
    node_attr="label",
    iterations=3,
    digest_size=16,
):
    if subgraph:
        return nx.weisfeiler_lehman_subgraph_hashes(
            G,
            edge_attr=edge_attr,
            node_attr=node_attr,
            iterations=iterations,
            digest_size=digest_size,
        )
    return nx.weisfeiler_lehman_graph_hash(
        G,
        edge_attr=edge_attr,
        node_attr=node_attr,
        iterations=iterations,
        digest_size=digest_size,
    )


def summarize(G, as_dict=False, as_dot=False):
    summary_graph = nx.snap_aggregation(
        G, node_attributes=("label",), edge_attributes=("label",)
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
    """Method to check if two graphs are similar. To simplify the problem, first the raw graph difference is computed to check if the graphs are the same.
    If not graph edit distance is computed with a fixed timeout to help answer the question
    """
    if not diff_graph(M1, M2, as_dict=True):
        return True
    distance = ged(M1, M2, upper_bound=upper_bound, timeout=timeout)
    if distance is None:
        return False
    return True
