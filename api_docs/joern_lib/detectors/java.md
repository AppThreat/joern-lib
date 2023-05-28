Module joern_lib.detectors.java
===============================

Functions
---------

    
`expand_annotations(rows)`
:   

    
`get_sinks_query(pattern='(?i).*(cloud|framework|data|http|net|socket|io|security|text|xml|json|proto|rpc|java).*')`
:   

    
`get_sources_query(pattern='(?i).*(cloud|framework|data|http|net|socket|io|security|text|xml|json|proto|rpc|java).*', file_pattern='(?i).*(controller|service).*', parameter_filter='typeFullName("java.lang.String")')`
:   

    
`list_http_filters(connection, annotations='javax\\.servlet\\.annotation\\.WebFilter')`
:   

    
`list_http_routes(connection, annotations='org\\.springframework\\.web\\.bind\\.annotation\\..*')`
:   

    
`list_methods(connection, modifier='public ', include_annotations=True, external=False, unresolved=True)`
:   

    
`list_sinks(connection, pattern='(?i).*(cloud|framework|data|http|net|socket|io|security|text|xml|json|proto|rpc|java).*')`
:   

    
`list_sources(connection, pattern='(?i).*(cloud|framework|data|http|net|socket|io|security|text|xml|json|proto|rpc|java).*', file_pattern='(?i).*(controller|service).*', parameter_filter='typeFullName("java.lang.String")')`
:   

    
`list_unresolved_external_methods(connection)`
:   

    
`suggest_flows(connection)`
: