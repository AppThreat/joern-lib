Module joern_lib.utils
======================
Common utilities

Functions
---------

    
`calculate_hash(content, digest_size=16)`
:   Function to calculate has using blake2b algorithm

    
`check_command(cmd)`
:   Method to check if command is available
    :return True if command is available in PATH. False otherwise

    
`collect_cpg_manifests(cpg_out_dir)`
:   Utility method to collect all the CPG manifests created in a directory

    
`colorize_dot_data(dot_data, scheme='paired9', colors=None, shapes=None, style='filled')`
:   Function to colorize dot data with Brewer color schemes
    
    This product includes color specifications and designs developed by Cynthia Brewer (http://colorbrewer.org/).

    
`exec_tool(tool_name, args=[], cwd=None)`
:   Method to execute external command

    
`expand_search_str(search_descriptor)`
:   Given a descriptor string or dict, this method converts into equivalent cpgql method

    
`find_files(src, src_ext_name)`
:   Utility method to find files

    
`fix_json(sout)`
:   Hacky method to convert the joern stdout string to json

    
`fix_query(query_str)`
:   Utility method to convert CPGQL queries to become json friendly

    
`parse_error(serr)`
:   Function to parse joern output and identify friendly error messages

    
`print_flows(result, symbol_highlight_color='bold red', filelocation_highlight_color='grey54', check_highlight_color='dim green')`
:   Function to print the data flows using a rich tree

    
`print_md(result)`
:   Function to print the result as a markdown

    
`print_table(result, title='', caption='', language='javascript')`
:   Function to print the result as a table

    
`print_tree(result, guide_style='bold bright_blue')`
:   Function to print call trees

    
`read_image(file_path)`
:   Function to read image file safely optionally converting binary formats to base64 string. Useful to render images in notebooks

    
`t(result, title='', caption='', language='javascript')`
:   Function to print the result as a table

    
`walk_tree(paths, tree, level_branches)`
:   Utility function to walk call tree