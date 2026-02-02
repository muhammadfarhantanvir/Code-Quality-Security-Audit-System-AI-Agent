# Deployment Instructions

This document explains how to deploy the Code Quality & Security Audit System using Docker and Vercel.

## Docker Deployment

### Prerequisites
- Docker Engine (version 20.10 or later)
- Docker Compose (version 2.0 or later)

### Quick Start with Docker

1. Clone the repository:
```bash
git clone https://github.com/muhammadfarhantanvir/Code-Quality-Security-Audit-System-AI-Agent.git
cd Code-Quality-Security-Audit-System-AI-Agent
```

2. Build and run with Docker Compose:
```bash
docker-compose up -d
```

3. Access the application:
   - Open your browser and navigate to `http://localhost:8501`
   - The Ollama service will be available at `http://localhost:11434`

### Production Deployment with Docker

For production environments, use the production Dockerfile:

```bash
docker build -f Dockerfile.prod -t code-audit-system .
docker run -d -p 8501:8501 --name code-audit-container code-audit-system
```

Or use the production compose file:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Using the Deployment Script

We've provided a convenient deployment script:

```bash
chmod +x deploy_docker.sh
./deploy_docker.sh
```

## Vercel Deployment

### Prerequisites
- A Vercel account
- Vercel CLI installed (`npm i -g vercel`)

### Deploy to Vercel

1. Install the Vercel CLI:
```bash
npm i -g vercel
```

2. Login to your Vercel account:
```bash
vercel login
```

3. Deploy the project:
```bash
vercel --prod
```

Alternatively, you can connect your GitHub repository to Vercel for automatic deployments.

### Manual Vercel Deployment

1. Create a `vercel.json` file in your project root (already included in this repository):
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python",
      "config": { "runtime": "python3.11" }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "STREAMLIT_SERVER_PORT": "3000",
    "STREAMLIT_SERVER_ADDRESS": "0.0.0.0",
    "PYTHONPATH": "."
  }
}
```

2. Run the deployment:
```bash
vercel --prod
```

## Configuration

### Environment Variables

The application supports the following environment variables:

- `OLLAMA_HOST`: Host address for the Ollama service (default: `ollama:11434`)
- `STREAMLIT_SERVER_PORT`: Port for the Streamlit server (default: `8501`)
- `STREAMLIT_SERVER_ADDRESS`: Address for the Streamlit server (default: `0.0.0.0`)
- `STREAMLIT_SERVER_HEADLESS`: Headless mode for Streamlit (default: `true`)

## Scaling

### Docker Scaling

To scale the application horizontally:

```bash
docker-compose up -d --scale code-audit-system=3
```

### Vercel Scaling

Vercel automatically handles scaling based on traffic. You can configure scaling limits in your Vercel dashboard.

## Monitoring

### Docker Logs

To monitor the application logs:

```bash
docker-compose logs -f
```

### Health Checks

The Docker containers include health checks that verify the application is running properly. You can check the health status with:

```bash
docker-compose ps
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**: If you get an error about ports being in use, change the port mapping in the docker-compose.yml file.

2. **Insufficient Memory**: The application may require significant memory for processing large codebases. Increase Docker's memory allocation if needed.

3. **Ollama Not Responding**: Ensure the Ollama service is running and accessible at the configured host/port.

### Debugging

To debug issues:

1. Check container logs: `docker-compose logs -f`
2. Verify container status: `docker-compose ps`
3. Test connectivity: `docker-compose exec code-audit-system ping ollama:11434`

## Updating

### Docker Updates

To update to the latest version:

```bash
git pull origin main
docker-compose build
docker-compose up -d
```

### Vercel Updates

With connected GitHub repository, Vercel will automatically deploy updates when you push to your main branch.

## Security Considerations

1. **Network Security**: The Docker setup includes a reverse proxy with Nginx for additional security.
2. **Container Security**: The application runs as a non-root user inside the container.
3. **Environment Variables**: Sensitive configurations should be managed through environment variables.

## Backup and Recovery

### Data Persistence

The Docker setup persists the audit results database in a volume. To backup:

```bash
docker-compose exec -T postgres pg_dump -U postgres audit_db > backup.sql
```

### Restoring Data

To restore from a backup:

```bash
docker-compose exec -i postgres psql -U postgres -d audit_db < backup.sql
```

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.