## Useful Commands

### Start Ollama
`ollama run llama3.2`

### Build and run the service with docker copose
`docker compose build && docker compose up`

### Build and run the docker container directly
`docker build . -t cll`
`docker run -d --name cll -p 80:80 cll`

## Notes

### Swagger
After running the docker container with the helplful command above, we can access swagger docs at localhost/docs in a local browser.

### Postgres
To install the psql client library: `brew install libpq`