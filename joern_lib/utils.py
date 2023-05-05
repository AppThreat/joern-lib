import os
import re
from hashlib import blake2b

from rich.console import Console
from rich.json import JSON
from rich.syntax import Syntax
from rich.table import Table
from rich.tree import Tree

console = Console(
    log_time=False,
    log_path=False,
    color_system="auto",
    width=int(os.getenv("COLUMNS", 280)),
)

check_labels_list = (
    "check",
    "valid",
    "sanit",
    "escape",
    "clean",
    "safe",
    "serialize",
    "convert",
    "authenticate",
    "authorize",
    "encode",
    "encrypt",
)


def t(result, title="", caption="", language="javascript"):
    return print_table(result, title, caption, language)


def print_table(result, title="", caption="", language="javascript"):
    table = Table(
        title=title,
        caption=caption,
        show_lines=True,
        expand=True,
        header_style="bold magenta",
    )
    cols_added = {}
    if isinstance(result, dict) and result.get("response"):
        console.print(result.get("response"))
    elif isinstance(result, list) and len(result):
        for row in result:
            if isinstance(row, dict):
                rows = []
                iterrows = []
                if row.get("_1"):
                    iterrows.append(row.get("_1"))
                if row.get("_2"):
                    iterrows.append(row.get("_2"))
                if not row.get("_1") and not row.get("_2"):
                    iterrows.append(row)
                for rowToUse in iterrows:
                    if isinstance(rowToUse, list):
                        if len(rowToUse):
                            if rowToUse[0].get("_label"):
                                if not cols_added.get(rowToUse[0].get("_label")):
                                    table.add_column(
                                        rowToUse[0].get("_label").lower(),
                                        overflow="fold",
                                    )
                                    cols_added[rowToUse[0].get("_label")] = True
                            elif rowToUse[0].get("name"):
                                if not cols_added.get(rowToUse[0].get("name")):
                                    table.add_column(
                                        rowToUse[0].get("name").lower(), overflow="fold"
                                    )
                                    cols_added[rowToUse[0].get("name")] = True
                            rows.append(JSON.from_data(rowToUse, default=""))
                    elif isinstance(rowToUse, dict):
                        for k, v in rowToUse.items():
                            # Simplify the table a bit for display
                            if k.startswith("ast") or k.startswith("column"):
                                continue
                            if not cols_added.get(k):
                                justify = "left"
                                if (
                                    k in ("id", "order")
                                    or "number" in k.lower()
                                    or "index" in k.lower()
                                ):
                                    justify = "right"
                                table.add_column(k, justify=justify, overflow="fold")
                                cols_added[k] = True
                            if isinstance(v, list) and len(v) == 0:
                                v = ""
                            if k == "code":
                                v = v.replace("<empty>", "")
                                rows.append(Syntax(v, language) if v else v)
                            elif k == "annotation" or isinstance(v, dict):
                                rows.append(JSON.from_data(v, default=""))
                            else:
                                rows.append(
                                    str(v).replace("<empty>", "")
                                    if v is not None
                                    else ""
                                )
                table.add_row(*rows)
            elif isinstance(row, list):
                table.add_row(row)
        console.print(table)
    else:
        console.print(result)


def print_md(result):
    if isinstance(result, dict) and result.get("response"):
        console.print(result.get("response"))
    else:
        console.print(result)


def walk_tree(paths, tree, level_branches):
    for path in paths:
        if not path:
            continue
        level = path.count("|    ")
        if level == 0:
            branch = tree
        elif level_branches.get(level - 1):
            branch = level_branches.get(level - 1)
            if not level_branches.get(level):
                level_branches[level] = branch
        branch.add(path.replace("+--- ", ""))


def print_tree(result, guide_style="bold bright_blue"):
    result = result.split("\n")
    if result:
        tree = Tree(result[0].replace("+--- ", ""), guide_style=guide_style)
        level_branches = {0: tree}
        if len(result) > 1:
            walk_tree(result[1:], tree, level_branches)
        console.print(tree)
    else:
        console.print("Empty tree")


def calculate_hash(content, digest_size=16):
    h = blake2b(digest_size=digest_size)
    h.update(content.encode())
    return h.hexdigest()


def print_flows(
    result,
    symbol_highlight_color="bold red",
    filelocation_highlight_color="grey54",
    check_highlight_color="dim green",
):
    if not result:
        return
    parsed_flows_list = []
    for res in result:
        useful_flows = []
        identifiers_list = []
        ftree = None
        floc_list = []
        flow_fingerprint_list = []
        if isinstance(res, dict) and res.get("_2"):
            location_list = res.get("_2")
            last_symbol = ""
            for idx, loc in enumerate(location_list):
                # Allow empty sink
                if loc.get("filename") == "<empty>" and idx < len(location_list) - 2:
                    continue
                symbol = loc.get("symbol", "").encode().decode("unicode_escape")
                if symbol.startswith("<operator"):
                    continue
                # Add the various computed fingerprints
                loc["fingerprints"] = {}
                code = (
                    loc.get("node", {})
                    .get("code", "")
                    .encode()
                    .decode("unicode_escape")
                    .strip()
                )
                methodFullName = loc.get("methodFullName", "").replace("<init>", "")
                methodShortName = loc.get("methodShortName", "").replace("<init>", "")
                class_name = loc.get("className")
                # If there is no class name but there is a method full name try to recover
                if not class_name and methodFullName:
                    class_name = methodFullName.split(":")[0]
                    if class_name.endswith("." + methodShortName):
                        class_name = re.sub(f".{methodShortName}$", "", class_name)
                node_name = loc.get("node", {}).get("name")
                # Highlight potential check methods
                if node_name and node_name in code and check_highlight_color:
                    for check_label in check_labels_list:
                        if check_label in node_name.lower():
                            code = code.replace(
                                node_name,
                                f"[{check_highlight_color}]{node_name}[/{check_highlight_color}]",
                            )
                if code == "<empty>":
                    code = ""
                for lk in ("methodShortName", "methodFullName", "symbol", "filename"):
                    if loc.get(lk):
                        loc["fingerprints"][lk] = calculate_hash(loc.get(lk))
                if code:
                    loc["fingerprints"]["code"] = calculate_hash(code)
                nodeLabel = loc.get("nodeLabel")
                if nodeLabel in ("METHOD_PARAMETER_IN", "CALL"):
                    floc = f"{loc.get('filename')}:{loc.get('lineNumber')}"
                    floc_key = f"{floc}|{symbol}"
                    # If the next entry in the flow is identical to this
                    # but better then ignore the current
                    if idx < len(location_list) - 1:
                        nextloc = location_list[idx + 1]
                        nextNodeLabel = nextloc.get("nodeLabel")
                        if nextNodeLabel in ("METHOD_PARAMETER_IN", "CALL"):
                            nextfloc = (
                                f"{nextloc.get('filename')}:{nextloc.get('lineNumber')}"
                            )
                            nextfloc_key = f"""{nextfloc}|{nextloc.get("symbol")}"""
                            if floc == nextfloc and len(floc_key) < len(nextfloc_key):
                                continue
                    if loc.get("filename") == "<empty>":
                        class_method_sep = "" if not methodShortName else "."
                        if symbol_highlight_color:
                            floc = f"{class_name}{class_method_sep}{methodShortName}( [{symbol_highlight_color}]{code}[/{symbol_highlight_color}] )"
                        else:
                            floc = f"{class_name}{class_method_sep}{methodShortName}( {code} )"
                    if floc_key not in floc_list:
                        if symbol == code and last_symbol and last_symbol != code:
                            symbol = last_symbol
                        if (
                            symbol
                            and symbol_highlight_color
                            and symbol in code
                            and symbol != code
                        ):
                            code = code.replace(
                                symbol,
                                f"[{symbol_highlight_color}]{symbol}[/{symbol_highlight_color}]",
                            )
                            last_symbol = symbol
                        if loc.get("filename") == "<empty>":
                            tree_content = floc
                        elif filelocation_highlight_color:
                            tree_content = f"[{filelocation_highlight_color}]{floc}[/{filelocation_highlight_color}] {code}"
                        else:
                            tree_content = f"{floc} {code}"
                        if not ftree:
                            ftree = Tree(tree_content)
                        else:
                            ftree.add(tree_content)
                        useful_flows.append(loc)
                        floc_list.append(floc_key)
                        if loc["fingerprints"].get("methodFullName"):
                            flow_fingerprint_list.append(
                                f'{loc["fingerprints"]["methodFullName"]}|{loc["fingerprints"]["symbol"]}'
                            )
                if (
                    nodeLabel in ("METHOD_PARAMETER_IN", "IDENTIFIER")
                    and symbol not in identifiers_list
                    and not symbol.startswith("$")
                    and not symbol.startswith("tmp")
                ):
                    identifiers_list.append(symbol)
                    last_symbol = symbol
        if ftree:
            flow_fingerprint_key = "-".join(flow_fingerprint_list)
            if flow_fingerprint_key not in parsed_flows_list:
                console.print(ftree)
                console.print("")
                parsed_flows_list.append(flow_fingerprint_key)


def expand_search_str(search_descriptor):
    """Given a descriptor string or dict, this method converts into equivalent cpgql method"""
    search_str = ""
    if isinstance(search_descriptor, str):
        if "." in search_descriptor:
            if (
                ":" in search_descriptor or "(" in search_descriptor
            ) and ".*" not in search_descriptor:
                search_str = f'.fullNameExact("{search_descriptor}")'
            else:
                search_str = f'.fullName("{search_descriptor}")'
        else:
            search_str = f'.name("{search_descriptor}")'
    elif isinstance(search_descriptor, dict):
        for k, v in search_descriptor.items():
            search_str = f'{search_str}.{k}("{v}")'
    return search_str
