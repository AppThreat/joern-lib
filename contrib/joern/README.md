# Joern

## Running Joern shell

```bash
docker run --rm -it -v /tmp:/tmp -v $(pwd):/app:rw --cpus=2 --memory=8g -t ghcr.io/appthreat/joern joern -J-Xmx8g
```

## Running Joern server

```bash
docker run --rm -it -v /tmp:/tmp -p 9000:9000 -v $(pwd):/app:rw --cpus=2 --memory=8g -t ghcr.io/appthreat/joern joern -J-Xmx8g --server --server-host 0.0.0.0 --server-port 9000
```
