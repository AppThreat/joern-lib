Module joern_lib.client
=======================

Functions
---------

    
`bulk_query(connection, query_list)`
:   Bulk query joern server

    
`create_cpg(connection, src, out_dir=None, lang=None, slice=None, slice_mode='Usages', auto_build=True, skip_sbom=False)`
:   Create CPG using cpggen server

    
`df(connection, source, sink, print_result=False, filter=None, check_labels=('check', 'valid', 'sanit', 'escape', 'clean', 'safe', 'serialize', 'convert', 'authenticate', 'authorize', 'encode', 'encrypt'))`
:   Execute reachableByFlows query. Optionally accepts filters which could be a raw conditional string or predefined keywords such as skip_control_structures, skip_cfg and skip_checks
    skip_control_structures: This adds a control structure filter `filter(m => m.elements.isControlStructure.size > 0)` to skip flows with control statements such if condition or break
    skip_cfg: This adds a cfg filter `filter(m => m.elements.isCfgNode.size > 0)` to skip flows with control flow graph nodes
    skip_checks: When used with check_labels parameter, this could filter flows containing known validation and sanitization code in the flow. Has a default list.

    
`flows(connection, source, sink)`
:   Execute reachableByFlows query

    
`flowsp(connection, source, sink, print_result=True)`
:   Execute reachableByFlows query and optionally print the result table

    
`get(base_url='http://localhost:9000', cpggen_url='http://localhost:7072', username=None, password=None)`
:   Function to create a connection to joern and cpggen server

    
`p(connection, query_str, title='', caption='')`
:   Function to print the result as a table

    
`q(connection, query_str)`
:   Query joern server and optionally print the result as a table if the query ends with .p

    
`query(connection, query_str)`
:   Query joern server

    
`reachable_by_flows(connection, source, sink, print_result=False)`
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