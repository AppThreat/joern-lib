Module joern_lib.detectors.java
===============================
Module to detect common functions used in java applications

Functions
---------

    
`expand_annotations(rows)`
:   Function to expand annotation nodes by identifying http methods and routes used

    
`get_sinks_query(pattern='(?i).*(cloud|framework|data|http|net|socket|io|security|text|xml|json|proto|rpc|java).*')`
:   Construct a CPGQL query to list the sinks for the application

    
`get_sources_query(pattern='(?i).*(cloud|framework|data|http|net|socket|io|security|text|xml|json|proto|rpc|java).*', file_pattern='(?i).*(controller|service).*', parameter_filter='typeFullName("java.lang.String")')`
:   Construct a CPGQL query to list the sources for the application

    
`list_http_filters(connection, annotations='javax\\.servlet\\.annotation\\.WebFilter')`
:   Retrieves the http filters in the application

    
`list_http_routes(connection, annotations='org\\.springframework\\.web\\.bind\\.annotation\\..*')`
:   Retrieves the http routes in the application

    
`list_methods(connection, modifier='public ', include_annotations=True, external=False, unresolved=True)`
:   Function to retrieve list of methods

    
`list_sinks(connection, pattern='(?i).*(cloud|framework|data|http|net|socket|io|security|text|xml|json|proto|rpc|java).*')`
:   Retrieves the list of sinks by filtering based on conventions

    
`list_sources(connection, pattern='(?i).*(cloud|framework|data|http|net|socket|io|security|text|xml|json|proto|rpc|java).*', file_pattern='(?i).*(controller|service).*', parameter_filter='typeFullName("java.lang.String")')`
:   Retrieves the list of sources by filtering based on conventions

    
`list_unresolved_external_methods(connection)`
:   Retrieves the methods without types resolved

    
`suggest_flows(connection)`
:   Suggest some data flows by identifying common sources and sinks