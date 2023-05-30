Module joern_lib.detectors.js
=============================
Module to detect common functions used in javascript/typescript applications

Functions
---------

    
`get_db_sinks(connection, sink='(?s)(?i).*(db|dao|mongo|mongoclient).*')`
:   Retrieve the list of common db sinks based on convention

    
`get_express_appvar(connection)`
:   Retrieve the variable that requires the express framework

    
`get_framework_appvar(connection, framework)`
:   Retrieve the variable that requires the framework

    
`get_framework_config(connection, app_var='app')`
:   Retrieve the variable that stores the framework configuration

    
`get_http_header_sinks(connection, sink='(?s)(?i).*res\\.(set|writeHead|setHeader).*')`
:   Retrieve the list of common http headers sinks based on convention

    
`get_http_sinks(connection, sink='(?s)(?i).*res\\.(append|attachment|cookie|clearCookie|download|end|format|get|json|jsonp|links|location|redirect|render|send|sendFile|sendStatus|set|status|type|vary).*')`
:   Retrieve the list of common http sinks based on convention

    
`get_http_sources(connection, source='(?s)(?i).*(req|ctx)\\.(originalUrl|path|protocol|route|secure|signedCookies|stale|subdomains|xhr|app|pipe|file|files|baseUrl|fresh|hostname|ip|url|ips|method|body|param|params|query|cookies|request).*')`
:   Retrieve the list of common http sources based on convention

    
`get_koa_appvar(connection)`
:   Retrieve the variable that requires the koa framework

    
`list_aws_modules(connection)`
:   Retrieve the list of AWS SDK modules

    
`list_http_routes(connection, app_vars='(app|router)', http_methods='(head|get|post|put|patch|delete|options)', include_middlewares=True)`
:   Retrieve the list of http routes

    
`list_imports(connection)`
:   Retrieve the list of import statements

    
`list_koa_modules(connection)`
:   Retrieve the list of koa framework modules

    
`list_nosql_collections(connection, db_list='(db|mongo)')`
:   Retrieve the list of NoSql database collections referred in the code

    
`list_requires(connection, require_var='require')`
:   Retrieve the list of require statements

    
`list_requires_location(connection, require_var='require')`
:   Retrieve the list of require statements and their locations

    
`list_sdk_modules(connection, sdk)`
:   Retrieve the list of modules for any sdk

    
`used_aws_modules(connection)`
:   Retrieve the list of used AWS SDK modules

    
`used_koa_modules(connection)`
:   Retrieve the list of used koa modules

    
`used_sdk_modules(connection, sdk)`
:   Retrieve the list of used SDK modules