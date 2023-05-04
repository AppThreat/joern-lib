Module joern_lib.client
=======================

Functions
---------

    
`bulk_query(connection, query_list)`
:   

    
`create_cpg(connection, src, out_dir, lang)`
:   

    
`df(connection, source, sink)`
:   

    
`fix_json(sout)`
:   

    
`fix_query(query_str)`
:   

    
`flows(connection, source, sink)`
:   

    
`flowsp(connection, source, sink, print=True)`
:   

    
`get(base_url='http://localhost:9000', cpggen_url='http://localhost:7072', username=None, password=None)`
:   

    
`p(connection, query_str, title='', caption='')`
:   

    
`parse_error(serr)`
:   

    
`q(connection, query_str)`
:   

    
`query(connection, query_str)`
:   

    
`reachableByFlows(connection, source, sink)`
:   

    
`receive(connection)`
:   

    
`send(connection, message)`
:   

Classes
-------

`Connection(cpggenclient, httpclient, websocket)`
:   

    ### Methods

    `close(self)`
    :

    `ping(self)`
    :