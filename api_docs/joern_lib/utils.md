Module joern_lib.utils
======================

Functions
---------

    
`calculate_hash(content, digest_size=16)`
:   

    
`colorize_dot_data(dot_data, scheme='paired9', colors={'method': '1', 'literal': '2', 'operator': '3', 'param': '4', 'identifier': '5', 'modifier': '6', 'unknown': '7', 'local': '7', 'type_ref': '8', 'return': '9'}, shapes={'method': 'box3d', 'literal': 'oval', 'operator': 'box', 'param': 'tab', 'identifier': 'note', 'modifier': 'rect', 'type_ref': 'component', 'return': 'cds'}, style='filled')`
:   Method to colorize dot data with Brewer color schemes
    
    This product includes color specifications and designs developed by Cynthia Brewer (http://colorbrewer.org/).

    
`expand_search_str(search_descriptor)`
:   Given a descriptor string or dict, this method converts into equivalent cpgql method

    
`fix_json(sout)`
:   Hacky method to convert the joern stdout string to json

    
`fix_query(query_str)`
:   Utility method to convert CPGQL queries to become json friendly

    
`parse_error(serr)`
:   Method to parse joern output and identify friendly error messages

    
`print_flows(result, symbol_highlight_color='bold red', filelocation_highlight_color='grey54', check_highlight_color='dim green')`
:   

    
`print_md(result)`
:   

    
`print_table(result, title='', caption='', language='javascript')`
:   

    
`print_tree(result, guide_style='bold bright_blue')`
:   

    
`read_image(file_path)`
:   Method to read image file safely optionally converting binary formats to base64 string. Useful to render images in notebooks

    
`t(result, title='', caption='', language='javascript')`
:   

    
`walk_tree(paths, tree, level_branches)`
: