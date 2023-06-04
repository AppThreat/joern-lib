Module joern_lib.detectors.common
=================================
Function to detect files, methods and patterns that are common across languages

Functions
---------

    
`create_tags(connection, query=None, call=None, method=None, tags=None)`
:   Function to create custom tags on nodes. Nodes could be selected based on a query, or call or method name.
    
    Tags could be a list of string or dictionary of key, value pairs

    
`export(connection, method=None, query=None, export_repr='pdg', colorize=True, as_graph=False)`
:   Function to export graph representations of a method or node

    
`get_call_tree(connection, method_name, n=3)`
:   Function to retrieve the call tree of a method

    
`get_calls(connection, pattern)`
:   Function to list calls

    
`get_complex_functions(connection, n=4)`
:   Function to retrieve complex methods/functions

    
`get_complex_methods(connection, n=4)`
:   Function to retrieve complex methods/functions

    
`get_functions_multiple_returns(connection)`
:   Function to retrieve methods with multiple return statements

    
`get_identifiers_in_file(connection, filename)`
:   Function to list identifiers in a file

    
`get_long_functions(connection, n=1000)`
:   Function to retrieve long methods/functions

    
`get_long_methods(connection, n=1000)`
:   Function to retrieve long methods/functions

    
`get_method(connection, method, as_graph=False, graph_repr='pdg')`
:   Retrieve the method optionally converting to networkx format

    
`get_method_callIn(connection, pattern)`
:   Function to list callIn locations

    
`get_methods_multiple_returns(connection)`
:   Function to retrieve methods with multiple return statements

    
`get_too_many_loops_functions(connection, n=4)`
:   Function to retrieve methods/functions with many loops

    
`get_too_many_loops_methods(connection, n=4)`
:   Function to retrieve methods/functions with many loops

    
`get_too_many_params_functions(connection, n=4)`
:   Function to retrieve methods/functions with many parameters

    
`get_too_many_params_methods(connection, n=4)`
:   Function to retrieve methods/functions with many parameters

    
`get_too_nested_functions(connection, n=4)`
:   Function to retrieve methods/functions that are nested

    
`get_too_nested_methods(connection, n=4)`
:   Function to retrieve methods/functions that are nested

    
`is_similar(connection, M1, M2, upper_bound=500, timeout=5)`
:   Convenient method to check if two methods are similar using graph edit distance

    
`list_annotations(connection)`
:   Retrieve the annotations

    
`list_arguments(connection)`
:   Retrieve the arguments

    
`list_assignments(connection)`
:   Retrieve all assignment operations

    
`list_calls(connection, search_descriptor=None)`
:   Retrieve the method calls

    
`list_config_files(connection)`
:   Retrieve the config files

    
`list_constructors(connection)`
:   Retrieve the list of constructors

    
`list_control_structures(connection)`
:   Retrieve the control structures

    
`list_custom_types(connection)`
:   Function to list all custom types

    
`list_declared_identifiers(connection)`
:   Retrieve the declared identifiers

    
`list_dependencies(connection)`
:   Retrieve the dependency nodes

    
`list_external_methods(connection)`
:   Retrieve the external methods

    
`list_files(connection, search_descriptor=None)`
:   Retrieve the list files in the CPG

    
`list_identifiers(connection)`
:   Retrieve the identifiers

    
`list_if_blocks(connection)`
:   Retrieve the if blocks

    
`list_imports(connection)`
:   Retrieve the import statements

    
`list_literals(connection)`
:   Retrieve the literals

    
`list_locals(connection)`
:   Retrieve the local variables

    
`list_members(connection)`
:   Retrieve the member variables

    
`list_metadatas(connection)`
:   Retrieve the metadata block

    
`list_methodReturns(connection)`
:   Retrieve the method return values

    
`list_method_refs(connection)`
:   Retrieve the method references

    
`list_methods(connection, search_descriptor=None, skip_operators=True, as_graph=False, graph_repr='pdg')`
:   Function to filter and retrieve a list of methods

    
`list_namespaces(connection)`
:   Retrieve the list of namespaces

    
`list_parameters(connection)`
:   Retrieve the list of parameters

    
`list_sensitive_literals(connection, pattern='(secret|password|token|key|admin|root)')`
:   Function to list sensitive literals

    
`list_tags(connection, name=None, value=None, is_call=False, is_method=False, is_parameter=False)`
:   Retrieve the list of tags assigned to call, method or parameters

    
`list_types(connection)`
:   Function to list types

    
`nx(connection, method, graph_repr='cpg14')`
:   Retrieve the methods as a networkx object