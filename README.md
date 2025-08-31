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
Data is stored in files under `data_dir` relative to where the command is run.

Common use case is to put this behind an nginx reverse proxy. Start the server with

```bash
python kv.py
```


## Client-side usage

To store `<value>` under `<key>`:
```bash
curl -X POST http://<host>/<key> -H "Content-Type: application/plain" -d "<value>"
```
If given key already exists, it will be overwritten.

To retrievet the value under `<key>`:
```bash
curl -X GET http://<host>/<key>
```
