Module joern_lib.client
=======================

Functions
---------

    
`bulk_query(connection, query_list)`
:   Bulk query joern server

    
`create_cpg(connection, src, out_dir, lang)`
:   Create CPG using cpggen server

    
`df(connection, source, sink, print_result=False)`
:   Execute reachableByFlows query

    
`fix_json(sout)`
:   Hacky method to convert the joern stdout string to json

    
`fix_query(query_str)`
:   Utility method to convert CPGQL queries to become json friendly

    
`flows(connection, source, sink)`
:   Execute reachableByFlows query

    
`flowsp(connection, source, sink, print_result=True)`
:   Execute reachableByFlows query and optionally print the result table

    
`get(base_url='http://localhost:9000', cpggen_url='http://localhost:7072', username=None, password=None)`
:   Method to create a connection to joern and cpggen server

    
`p(connection, query_str, title='', caption='')`
:   Method to print the result as a table

    
`parse_error(serr)`
:   Method to parse joern output and identify friendly error messages

    
`q(connection, query_str)`
:   Query joern server and optionally print the result as a table if the query ends with .p

    
`query(connection, query_str)`
:   Query joern server

    
`reachableByFlows(connection, source, sink, print_result=False)`
:   Execute reachableByFlows query

    
`receive(connection)`
:   Receive message from the joern server

    
`send(connection, message)`
:   Send message to the joern server via websocket

Classes
-------

`Connection(cpggenclient, httpclient, websocket)`
:   Connection object to hold following connections:
       - Websocket to joern server
       - http connection to joern server
       - http connection to cpggen server

    ### Methods

    `close(self)`
    :   Close all connections

    `ping(self)`
    :   Send websocket ping message