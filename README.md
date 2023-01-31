# Quick Start

1. Ensure a recent version of Python is installed.

2. Create a Python virtual environment:
   ```console
   $ python3 -m venv .venv
   $ source .venv/bin/activate
   $ pip install -r requirements.txt
   ```

   ```powershell
   PS> python -m venv .venv
   PS> .\.venv\Scripts\Activate.ps1
   PS> pip install -r requirements.txt
   ```

3. Set the appropriate environment variables:
   ```console
   $ export MONGO_URI="mongodb://server_name:27017"
   $ export REDIS_URI="redis://user:pass@server_name:6379"
   ```

   ```powershell
   PS> $env:MONGO_URI = "mongodb://server_name:27017"
   PS> $env:REDIS_URI = "redis://user:pass@server_name:6379"
   ```

4. Start the Flask application:
   ```console
   $ export FLASK_APP="main.py"
   $ flask --debug run
   ```

   ```powershell
   PS> $env:FLASK_APP = "main.py"
   PS> flask --debug run
   ```

# Notes

You can see what the associated backend URIs are by using the `/status` endpoint on the API.

```console
$ curl http://localhost:5000/status
```

```json
{
  "backend": {
    "MONGO_URI": "mongodb://root:********@10.0.0.117:27017",
    "REDIS_URI": "redis://10.0.0.117:6379"
  },
  "version": "1.0.0",
  "uptime": "14 minutes"
}
```

# Docker Compose

You can also spin up the application using the `docker-compose.yaml` file in the `docker` directory.  This will build the
application and spin up the associated services needed to run the application.  If you make changes to the server or want
to test out new and exciting things, you can pass the `--build` option to rebuild the server container.

```console
$ cd docker
$ docker compose up --build
```

```powershell
PS> cd docker
PS> docker compose up --build
```
