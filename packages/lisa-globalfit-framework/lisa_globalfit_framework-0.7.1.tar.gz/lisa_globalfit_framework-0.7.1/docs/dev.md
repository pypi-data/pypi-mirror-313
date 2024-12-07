# Development guide

## Third-party components

* [NATS Server](https://docs.nats.io/)

Install it from binary distribution.

```console
NATS_VER="v2.10.22"
curl -L "https://github.com/nats-io/nats-server/releases/download/$NATS_VER/nats-server-$NATS_VER-linux-amd64.zip" -o nats-server.zip
unzip nats-server.zip -d nats-server
```

* [NATS CLI](https://docs.nats.io/using-nats/nats-tools/nats_cli)

```console
NATS_VER="0.1.5"
curl -L "https://github.com/nats-io/natscli/releases/download/v$NATS_VER/nats-$NATS_VER-linux-amd64.zip" -o nats-cli.zip
unzip nats-cli.zip
```

Run it using JetStream with a temporary store

```console
nats-server --jetstream --store_dir $(mktemp -d)
```

* [Argo CLI](https://argo-workflows.readthedocs.io/en/latest/walk-through/argo-cli/)

```console
ARGO_CLI_VER="3.5.11"
curl -sLO "https://github.com/argoproj/argo-workflows/releases/download/v$ARGO_CLI_VER/argo-linux-amd64.gz"
gunzip argo-linux-amd64.gz
chmod +x argo-linux-amd64
```

* [SQLite](https://www.sqlite.org/index.html)

```console
SQLITE_VER="3450200"
curl -L "https://www.sqlite.org/2024/sqlite-amalgamation-$SQLITE_VER.zip" -O
unzip sqlite-amalgamation-$SQLITE_VER.zip
cd sqlite-amalgamation-$SQLITE_VER
gcc sqlite3.c -lpthread -ldl -lm -fPIC -shared -o libsqlite3.so.0
export LD_LIBRARY_PATH="$(realpath .):$LD_LIBRARY_PATH" # in your shell profile
```

## Editable installation

```console
uv sync
uv tool run pre-commit install
```

## Tools

* [Visualize](https://mermaid.live) class diagrams

```console
uv run pyreverse --output mmd src/lisa/globalfit/framework
```
