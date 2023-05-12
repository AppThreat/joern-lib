Module joern_lib.graph
======================

Functions
---------

    
`convert_dot(data)`
:   Method to convert dot data into graph

    
`diff(first_graph, second_graph, include_common=False, as_dict=False, as_dot=False)`
:   

    
`diff_graph(first_graph, second_graph, include_common=False, as_dict=False, as_dot=False)`
:   

    
`ged(first_graph, second_graph, timeout=5, upper_bound=500)`
:   

    
`gep(first_graph, second_graph, upper_bound=500)`
:   

    
`hash(G, subgraph=False, edge_attr='label', node_attr='label', iterations=3, digest_size=16)`
:   

    
`is_similar(M1, M2, upper_bound=500, timeout=5)`
:   Method to check if two graphs are similar. To simplify the problem, first the raw graph difference is computed to check if the graphs are the same.
    If not graph edit distance is computed with a fixed timeout to help answer the question

    
`node_match_fn(n1, n2)`
:   

    
`summarize(G, as_dict=False, as_dot=False)`
:   

    
`write_dot(G, path)`
: