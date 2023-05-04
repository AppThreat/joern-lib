Module joern_lib.detectors.js
=============================

Functions
---------

    
`get_db_sinks(connection, sink='(?s)(?i).*(db|dao|mongo|mongoclient).*')`
:   

    
`get_express_appvar(connection)`
:   

    
`get_framework_appvar(connection, framework)`
:   

    
`get_framework_config(connection, app_var='app')`
:   

    
`get_http_header_sinks(connection, sink='(?s)(?i).*res\\.(set|writeHead|setHeader).*')`
:   

    
`get_http_sinks(connection, sink='(?s)(?i).*res\\.(append|attachment|cookie|clearCookie|download|end|format|get|json|jsonp|links|location|redirect|render|send|sendFile|sendStatus|set|status|type|vary).*')`
:   

    
`get_http_sources(connection, source='(?s)(?i).*(req|ctx)\\.(originalUrl|path|protocol|route|secure|signedCookies|stale|subdomains|xhr|app|pipe|file|files|baseUrl|fresh|hostname|ip|url|ips|method|body|param|params|query|cookies|request).*')`
:   

    
`get_koa_appvar(connection)`
:   

    
`list_aws_modules(connection)`
:   

    
`list_http_routes(connection, app_vars='(app|router)', http_methods='(head|get|post|put|patch|delete|options)', include_middlewares=True)`
:   

    
`list_imports(connection)`
:   

    
`list_koa_modules(connection)`
:   

    
`list_nosql_collections(connection, db_list='(db|mongo)')`
:   

    
`list_requires(connection, require_var='require')`
:   

    
`list_requires_location(connection, require_var='require')`
:   

    
`list_sdk_modules(connection, sdk)`
:   

    
`used_aws_modules(connection)`
:   

    
`used_koa_modules(connection)`
:   

    
`used_sdk_modules(connection, sdk)`
: