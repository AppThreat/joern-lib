Module joern_lib.detectors.common
=================================

Functions
---------

    
`create_tags(connection, query=None, call=None, method=None, tags=None)`
:   Method to create custom tags on nodes. Nodes could be selected based on a query, or call or method name.
    
    Tags could be a list of string or dictionary of key, value pairs

    
`export(connection, method=None, query=None, repr='pdg', colorize=True)`
:   Method to export graph representations of a method or node

    
`get_call_tree(connection, method_name, n=3)`
:   

    
`get_calls(connection, pattern)`
:   

    
`get_complex_functions(connection, n=4)`
:   

    
`get_complex_methods(connection, n=4)`
:   

    
`get_functions_multiple_returns(connection)`
:   

    
`get_identifiers_in_file(connection, filename)`
:   

    
`get_long_functions(connection, n=1000)`
:   

    
`get_long_methods(connection, n=1000)`
:   

    
`get_method(connection, method, as_graph=False, graph_repr='pdg')`
:   

    
`get_method_callIn(connection, pattern)`
:   

    
`get_methods_multiple_returns(connection)`
:   

    
`get_too_many_loops_functions(connection, n=4)`
:   

    
`get_too_many_loops_methods(connection, n=4)`
:   

    
`get_too_many_params_functions(connection, n=4)`
:   

    
`get_too_many_params_methods(connection, n=4)`
:   

    
`get_too_nested_functions(connection, n=4)`
:   

    
`get_too_nested_methods(connection, n=4)`
:   

    
`is_similar(connection, M1, M2, upper_bound=500, timeout=5)`
:   Convenient method to check if two methods are similar using graph edit distance

    
`list_annotations(connection)`
:   

    
`list_arguments(connection)`
:   

    
`list_assignments(connection)`
:   

    
`list_calls(connection, search_descriptor=None)`
:   

    
`list_config_files(connection)`
:   

    
`list_constructors(connection)`
:   

    
`list_control_structures(connection)`
:   

    
`list_custom_types(connection)`
:   

    
`list_declared_identifiers(connection)`
:   

    
`list_dependencies(connection)`
:   

    
`list_external_methods(connection)`
:   

    
`list_files(connection, search_descriptor=None)`
:   

    
`list_identifiers(connection)`
:   

    
`list_if_blocks(connection)`
:   

    
`list_imports(connection)`
:   

    
`list_literals(connection)`
:   

    
`list_locals(connection)`
:   

    
`list_members(connection)`
:   

    
`list_metadatas(connection)`
:   

    
`list_methodReturns(connection)`
:   

    
`list_method_refs(connection)`
:   

    
`list_methods(connection, search_descriptor=None, skip_operators=True, as_graph=False, graph_repr='pdg')`
:   

    
`list_namespaces(connection)`
:   

    
`list_parameters(connection)`
:   

    
`list_sensitive_literals(connection, pattern='(secret|password|token|key|admin|root)')`
:   Method to list sensitive literals

    
`list_tags(connection, name=None, value=None, is_call=False, is_method=False, is_parameter=False)`
:   

    
`list_types(connection)`
:   

    
`nx(connection, method, graph_repr='cpg14')`
: