Module joern_lib.workspace
==========================
Functions to perform workspace related operations

Functions
---------

    
`cpg_exists(connection, project_name)`
:   Function to check if a CPG exists in the workspace

    
`create_atom(connection, src, out_dir=None, languages='autodetect', project_name=None)`
:   Function to create atom using atomgen server

    
`create_cpg(connection, src, out_dir=None, languages='autodetect', project_name=None, slice=None, slice_mode='Usages', auto_build=True, skip_sbom=True, use_atom=False)`
:   Function to create CPG using cpggen server

    
`delete_project(connection, project_name)`
:   Function to delete a project

    
`dir_exists(connection, dir_name)`
:   Function to check if a directory exists and is accessible from the joern server

    
`extract_dir(res)`
:   Extract the directory name from the CPGQL response

    
`from_string(connection, code_snippet, language='jssrc')`
:   Function to import string

    
`get_active_project(connection)`
:   Function to retrieve active project

    
`get_overlay_dir(connection, project_name)`
:   Function to retrieve the overlays of a project

    
`get_path(connection)`
:   Function to retrieve the path to a workspace

    
`import_code(connection, directory, project_name=None)`
:   Function to import code to joern

    
`import_cpg(connection, cpg_path, project_name=None)`
:   Function to import CPG

    
`ls(connection)`
:   Retrieves the list of CPGs in the workspace

    
`reset(connection)`
:   Function to reset workspace

    
`set_active_project(connection, project_name)`
:   Function to set active project

    
`slice_cpg(connection, src, out_dir=None, languages='autodetect', project_name=None, slice_mode='Usages')`
:   Function to slice the CPG based on a slice mode