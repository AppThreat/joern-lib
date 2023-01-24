import os

from rich import box
from rich.console import Console
from rich.markdown import Markdown
from rich.markup import escape
from rich.panel import Panel
from rich.progress import Progress
from rich.syntax import Syntax
from rich.table import Table
from rich.terminal_theme import MONOKAI
from rich.theme import Theme
from rich.tree import Tree

console = Console(
    log_time=False,
    log_path=False,
    color_system="auto",
    width=int(os.getenv("COLUMNS", 280)),
)


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
                rowToUse = row
                if row.get("_2"):
                    rowToUse = row.get("_2")
                elif row.get("_1"):
                    rowToUse = row.get("_1")
                for k, v in rowToUse.items():
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
                        rows.append(Syntax(v, language))
                    else:
                        rows.append(str(v) if v is not None else "")
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
