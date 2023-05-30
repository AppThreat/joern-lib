Module joern_lib.detectors.python
=================================
Module to detect common functions used in python applications

Functions
---------

    
`expand_decorators(rows)`
:   Function to expand decorators to identify http methods and routes

    
`list_decorator_location(connection, decorator, is_method_ref=True)`
:   Function to list the methods and their location for a given decorator

    
`list_dict_assignment_location(connection, key=None, is_literal=True)`
:   Function to list locations where a dictionary key is assigned a hardcoded value

    
`list_http_routes(connection, decorators='route')`
:   Function to list http routes in the application