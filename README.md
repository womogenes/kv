# kv

Self-hosted key-value store with a REST API.

## Usage

```bash
curl -X POST http://<host>/<key> -H "Content-Type: application/plain" -d "value"
```

```bash
curl -X GET http://<host>/<key>
```

Common use case is to put this behind an nginx reverse proxy.
