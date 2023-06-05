Module joern_lib.graph
======================
Module to work with networkx graph data

Functions
---------

    
`convert_dot(data)`
:   Function to convert dot data into graph

    
`convert_graphml(gml_file, force_multigraph=False, as_graph=True, as_adjacency_data=False)`
:   Function to convert graphml to networkx

    
`diff(first_graph, second_graph, include_common=False, as_dict=False, as_dot=False)`
:   Function to compute the difference between two graphs

    
`diff_graph(first_graph, second_graph, include_common=False, as_dict=False, as_dot=False)`
:   Function to compute the difference between two graphs and optionally convert the result to dict or dot format

    
`ged(first_graph, second_graph, timeout=5, upper_bound=500)`
:   Function to compute the difference based on graph edit distance algorithm

    
`gep(first_graph, second_graph, upper_bound=500)`
:   Function to compute the difference based on optimal edit path algorithm

    
`get_node_label(n)`
:   Retrieve a label for the node from various data attributes

    
`graph_hash(G, edge_attr_fn=None, node_attr_fn=None, iterations=3, digest_size=16)`
:   Return Weisfeiler Lehman (WL) graph hash

    
`hash(G, subgraph=False, edge_attr_fn=<function get_node_label>, node_attr_fn=<function get_node_label>, iterations=3, digest_size=16)`
:   Function to compute the hashes for a graph using Weisfeiler Lehman hashing algorithm

    
`is_similar(M1, M2, upper_bound=500, timeout=5)`
:   Function to check if two graphs are similar. To simplify the problem, first the raw graph difference is computed to check if the graphs are the same.
    If not graph edit distance is computed with a fixed timeout to help answer the question

    
`node_match_fn(n1, n2)`
:   

    
`subgraph_hashes(G, edge_attr_fn=None, node_attr_fn=None, iterations=3, digest_size=16)`
:   Return a dictionary of subgraph hashes by node.

    
`summarize(G, as_dict=False, as_dot=False)`
:   Function to summarize the graph based on node labels

    
`to_pyg(G, group_node_attrs=None, group_edge_attrs=None)`
:   Converts a :obj:`networkx.Graph` or :obj:`networkx.DiGraph` to a
    :class:`torch_geometric.data.Data` instance.

    
`write_dot(G, path)`
:   Function to export graph as dot