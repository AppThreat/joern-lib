# Introduction

This project offers a high level python library to interact with a Joern [server](https://docs.joern.io/server). Several API methods are offered to perform code analysis on complex code bases without knowing [CPGQL](https://docs.joern.io/c-syntaxtree).

```
pip install joern-lib
```

The repository includes docker compose configuration to interactively query the joern server with polynote notebooks.

![polynote interface](docs/note1.jpg)

![polynote interface](docs/note2.jpg)

![polynote interface](docs/note3.jpg)

![polynote interface](docs/note4.jpg)

![polynote interface](docs/sqli.jpg)

![polynote interface](docs/repl.jpg)

![polynote interface](docs/call-tree.jpg)

## Usage

Run joern server and polynote locally.

```
git clone https://github.com/appthreat/joern-lib.git
# Edit docker-compose.yml to set sources directory
docker compose up -d

# podman-compose up --build
```

Navigate to http://localhost:8192 for an interactive polynote notebook. You could open one of the sample notebooks from the [contrib](./contrib/polynote/notebooks/joern-notes/) directory to learn about Joern server and this library.

### Common steps

```
python -m asyncio
```

Execute single query

```
from joern_lib import client, workspace, utils
from joern_lib.detectors import common as cpg

connection = await client.get("http://localhost:9000", "http://localhost:7072", "admin", "admin")

# connection = await client.get("http://localhost:9000")

res = await client.q(connection, "val a=1");

# {'response': 'a: Int = 1\n'}
```

Execute bulk query

```
res = await client.bulk_query(connection, ["val a=1", "val b=2", "val c=a+b"]);
# [{'response': 'a: Int = 1\n'}, {'response': 'b: Int = 2\n'}, {'response': 'c: Int = 3\n'}]
```

### Workspace

List workspaces

```
res = await workspace.list(connection)
```

Get workspace path

```
res = await workspace.get_path(connection)
# /workspace (Response would be parsed)
```

Check if cpg exists

```
await workspace.cpg_exists(connection, "NodeGoat")
```

Import code for analysis

```
res = await workspace.import_code(connection, "/app", "NodeGoat")
# True
```

Import an existing CPG for analysis

```
res = await workspace.import_cpg(connection, "/app/sandbox/crAPI/cpg_out/crAPI-python-cpg.bin.zip", "crAPI-python")
```

Create a CPG with a remote cpggen server

```
res = await workspace.create_cpg(connection, "/app/sandbox/crAPI", out_dir="/app/sandbox/crAPI/cpg_out", languages="python", project_name="crAPI-python")
```

### CPG core

List files

```
res = await cpg.list_files(connection)
# list of files
```

Print call tree

```
res = await cpg.get_call_tree(connection, "com.example.vulnspring.WebController.issue:java.lang.String(org.springframework.ui.Model,java.lang.String)")
utils.print_tree(res)
```

### Java specific

```
from joern_lib.detectors import java
```

List http routes

```
await java.list_http_routes(connection)
```

### JavaScript specific

```
from joern_lib.detectors import js
```

List http routes

```
await js.list_http_routes(connection)
```

Name of the variable containing express()

```
await js.get_express_appvar(connection)
```

List of require statements

```
await js.list_requires(connection)
```

List of import statements

```
await js.list_imports(connection)
```

List of NoSQL DB collection names

```
await js.list_nosql_collections(connection)
```

Get HTTP sources

```
await js.get_http_sources(connection)
await js.get_http_sinks(connection)
```

### AWS

Requires TypeScript project

```
await js.list_aws_modules(connection)
```

## Troubleshooting

### No response from server

If Joern server stops responding after a while restart docker.

```
docker compose down
docker compose up -d
```

### Websockets connection closed error

Adding asyncio.sleep(0) seems to fix such errors.

```
# Workaround to fix websockets.exceptions.ConnectionClosedError
await asyncio.sleep(0)
```
