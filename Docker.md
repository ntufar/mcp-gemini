# Docker Deployment

You can deploy the MCP Server using Docker or Docker Compose.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (optional, for easier deployment)

## Quick Start with Docker Compose

1. Create a directory for your data:
   ```bash
   mkdir data
   ```

2. Place any files you want the server to access in the `data/` directory

3. Run the server using Docker Compose:
   ```bash
   docker-compose up -d
   ```

4. The server will be accessible at `http://localhost:8000`

## Manual Docker Run

If you prefer to run the container manually:

```bash
# Build the image
docker build -t mcp-server .

# Run the container with data volume
docker run -d -p 8000:8000 -v $(pwd)/data:/data:ro -e MCP_SERVER_ROOT_DIR=/data --name mcp-server mcp-server
```

## Managing the Container

### View Logs

To view the server logs:

With Docker Compose:
```bash
docker-compose logs -f
```

With Docker:
```bash
docker logs -f mcp-server
```

### Stop the Container

To stop the server:

With Docker Compose:
```bash
docker-compose down
```

With Docker:
```bash
docker stop mcp-server
```

## Configuration

The server can be configured using environment variables:

- `MCP_SERVER_ROOT_DIR`: Sets the root directory that the server can access (default: `/app`)

## Security Note

In the example configurations, the data volume is mounted as read-only (`:ro`) as a security measure. Modify the volume mount as needed based on your requirements, keeping security in mind.