# kv

Self-hosted key-value store with a REST API.

## Configuration

Defaults are in `config.json` but this works without a config file.

```json
{
  "port": 8000,
  "data_dir": "data"
}
```

Common use case is to put this behind an nginx reverse proxy.


## Usage

To store <value> under <key>:
```bash
curl -X POST http://<host>/<key> -H "Content-Type: application/plain" -d "<value>"
```
If given key already exists, it will be overwritten.

To retrieve <value> under <key>:
```bash
curl -X GET http://<host>/<key>
```

