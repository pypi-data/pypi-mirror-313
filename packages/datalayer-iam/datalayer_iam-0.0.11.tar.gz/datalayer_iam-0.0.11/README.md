[![Datalayer](https://assets.datalayer.tech/datalayer-25.svg)](https://datalayer.io)

# Ξ 🛂 Datalayer IAM

Datalayer `IAM` service delivers `Identity` and `Access` (aka `Authentication` and `Authorization`) to the Datalayer platform.

```bash
make dev
make start
open http://localhost:9700/api/iam/version
```

## Development

### IAM as middleware

The devcontainer docker compose file defines traefik as a reverse proxy behind which is added a whoami service.

The proxy check for valid user authentication by adding a forwardAuth middleware that will ask datalayer IAM if the request is allowed or not.

To test it, assuming you are executing this project with VS Code on dev container,

1. Uncomment the services _reverse-proxy_ and _whoami_ in the dev [docker-compose](.devcontainer/docker-compose.yml). Then restart the dev container.

1. Update your local file `/etc/hosts` to add:

```
127.0.1.1       whoami.example.com
```

3. Start IAM server

```sh
cd iam
make start
```

4. Create an datalayer user and get a JWT token for it.

5. With a terminal (outside of VS Code), you can now test the forwardAuth middleware

   a. Forbidden case: `curl http://whoami.example.com:9080`
   b. Allowed case: `curl -H 'Authorization: Bearer <JWT token>' http://whoami.example.com:9080`
