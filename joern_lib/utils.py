import os
import re
from hashlib import blake2b

import orjson
from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.tree import Tree

console = Console(
    log_time=False,
    log_path=False,
    color_system="auto",
    width=int(os.getenv("COLUMNS", 180)),
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
        symbol = ""
        last_symbol = ""
        node_name = ""
        code = ""
        last_code = ""
        if isinstance(res, dict) and res.get("_2"):
            location_list = res.get("_2")
            for idx, loc in enumerate(location_list):
                # Allow empty sink
                filename = loc.get("filename", "")
                if filename == "<empty>" and idx < len(location_list) - 2:
                    continue
                symbol = loc.get("symbol", "").encode().decode("unicode_escape")
                node_name = loc.get("node", {}).get("name")
                if symbol.startswith("<operator"):
                    continue
                # Add the various computed fingerprints
                loc["fingerprints"] = {}
                code = (
                    (
                        loc.get("node", {})
                        .get("code", "")
                        .encode()
                        .decode("unicode_escape")
                        .strip()
                    )
                    .replace("\t", "")
                    .replace("\n", " ")
                )
                if code == last_code:
                    continue
                methodFullName = loc.get("methodFullName", "").replace("<init>", "")
                methodShortName = loc.get("methodShortName", "").replace("<init>", "")
                class_name = loc.get("className")
                # If there is no class name but there is a method full name try to recover
                if not class_name and methodFullName:
                    class_name = methodFullName.split(":")[0]
                    if class_name.endswith("." + methodShortName):
                        class_name = re.sub(f".{methodShortName}$", "", class_name)
                # Highlight potential check methods
                if check_highlight_color:
                    for check_label in check_labels_list:
                        if check_label in methodShortName:
                            methodShortName = methodShortName.replace(
                                methodShortName,
                                f"[{check_highlight_color}]{methodShortName}[/{check_highlight_color}]",
                            )
                        if node_name and node_name in code:
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
                if nodeLabel in ("METHOD_PARAMETER_IN", "CALL") or (
                    filename.endswith(".py")
                    and nodeLabel == "IDENTIFIER"
                    and (idx == 0 or idx == len(location_list) - 1)
                ):
                    floc = f"{loc.get('filename')}:{loc.get('lineNumber')} {methodShortName}()"
                    floc_key = f"{floc}|{symbol}"
                    # If the next entry in the flow is identical to this
                    # but better then ignore the current
                    if idx < len(location_list) - 1:
                        nextloc = location_list[idx + 1]
                        nextNodeLabel = nextloc.get("nodeLabel")
                        if nextNodeLabel in (
                            "METHOD_PARAMETER_IN",
                            "CALL",
                            "IDENTIFIER",
                        ):
                            nextfloc = (
                                f"{nextloc.get('filename')}:{nextloc.get('lineNumber')}"
                            )
                            nextfloc_key = f"""{nextfloc}|{nextloc.get("symbol")}"""
                            if floc == nextfloc and (
                                floc_key == nextfloc_key
                                or len(floc_key) < len(nextfloc_key)
                            ):
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
                            and (symbol in code or symbol in identifiers_list)
                        ):
                            last_code = code
                            code = (
                                code.replace(
                                    f'"{symbol}',
                                    f'"[{symbol_highlight_color}]{symbol}[/{symbol_highlight_color}]',
                                )
                                .replace(
                                    f"({symbol},",
                                    f"( [{symbol_highlight_color}]{symbol} [/{symbol_highlight_color}],",
                                )
                                .replace(
                                    f"{symbol})",
                                    f"[{symbol_highlight_color}]{symbol}[/{symbol_highlight_color}] )",
                                )
                                .replace(
                                    f"{symbol},",
                                    f"[{symbol_highlight_color}]{symbol}[/{symbol_highlight_color}] ,",
                                )
                                .replace(
                                    f"{symbol}[",
                                    f"[{symbol_highlight_color}]{symbol}[/{symbol_highlight_color}][",
                                )
                                .replace(
                                    f"&{symbol}",
                                    f"[{symbol_highlight_color}]&{symbol}[/{symbol_highlight_color}]",
                                )
                                .replace(
                                    f"*{symbol}",
                                    f"[{symbol_highlight_color}]*{symbol}[/{symbol_highlight_color}]",
                                )
                                .replace(
                                    f" {symbol} ",
                                    f" [{symbol_highlight_color}]{symbol}[/{symbol_highlight_color}] ",
                                )
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
                    and symbol != "NULL"
                ):
                    identifiers_list.append(symbol)
                    last_symbol = symbol
        if ftree:
            flow_fingerprint_key = "-".join(flow_fingerprint_list)
            if flow_fingerprint_key not in parsed_flows_list:
                if identifiers_list:
                    console.print(
                        Panel(
                            "\n".join(identifiers_list),
                            expand=False,
                            title="Tainted Identifiers",
                        )
                    )
                console.print(Panel(ftree, expand=False, title="Data Flow"))
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


def fix_json(sout):
    """Hacky method to convert the joern stdout string to json"""
    source_sink_mode = False
    try:
        if "defined function source" in sout:
            source_sink_mode = True
            sout = sout.replace("defined function source\n", "")
            sout = sout.replace("defined function sink\n", "")
        else:
            sout = sout.replace(r'"\"', '"').replace(r'\""', '"')
        if ': String = "[' in sout or ": String = [" in sout:
            if ": String = [" in sout:
                sout = sout.split(": String = ")[-1]
            elif source_sink_mode:
                sout = (
                    sout.replace(r"\"", '"')
                    .replace('}]}]"', "}]}]")
                    .replace('\\"', '"')
                )
                if ': String = "[' in sout:
                    sout = sout.split(': String = "')[-1]
            else:
                sout = sout.split(': String = "')[-1][-1]

        elif "tree: ListBuffer" in sout:
            sout = sout.split(": String = ")[-1]
            if '"""' in sout:
                sout = sout.replace('"""', "")
            return sout
        elif 'String = """[' in sout:
            tmpA = sout.split("\n")[1:-2]
            sout = "[ " + "\n".join(tmpA) + "]"
        return orjson.loads(sout)
    except Exception:
        return {"response": sout}


def fix_query(query_str):
    """Utility method to convert CPGQL queries to become json friendly"""
    if "\\." in query_str and "\\\\." not in query_str:
        query_str = query_str.replace("\\.", "\\\\.")
    if (query_str.startswith("cpg.") or query_str.startswith("({cpg.")) and (
        ".toJson" not in query_str
        and ".plotDot" not in query_str
        and not query_str.endswith(".p")
        and ".store" not in query_str
        and "def" not in query_str
        and "printCallTree" not in query_str
    ):
        query_str = f"{query_str}.toJsonPretty"
    if os.getenv("POLYNOTE_VERSION") or os.getenv("AT_DEBUG_MODE") in ("true", "1"):
        console.print(
            Panel(Syntax(query_str, "scala"), expand=False, title="CPGQL Query")
        )
    return query_str


def parse_error(serr):
    """Method to parse joern output and identify friendly error messages"""
    if "No projects loaded" in serr:
        return """ERROR: Import code using import_code api. Usage: await workspace.import_code(connection, directory_name, app_name)"""
    if "No CPG loaded" in serr:
        return """ERROR: Import cpg using import_cpg or create_cpg api."""
    return serr
