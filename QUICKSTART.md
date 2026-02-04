# Quick Start Guide

## Prerequisites

- Docker and Docker Compose installed
- At least 2GB free disk space
- Ports 3000 and 8000 available

## Step 1: Start the Application

```bash
docker-compose up
```

This will:
- Build the backend Docker image
- Build the frontend Docker image
- Start both services

## Step 2: Access the Application

Once the containers are running:

1. **Open the Frontend Dashboard**: http://localhost:3000
2. **View API Documentation**: http://localhost:8000/docs
3. **Check Health**: http://localhost:8000/health

## Step 3: Test Normalization

### Using the Web UI

1. Go to http://localhost:3000
2. Select a locale (Hindi or Tamil)
3. Enter text like: `₹250 on 12/03/2024 at 10:30AM`
4. Click "Normalize"
5. View the normalized text and SSML output

### Using the API

```bash
# Normalize text
curl -X POST "http://localhost:8000/normalize" \
  -H "Content-Type: application/json" \
  -d '{"locale": "hi-IN", "text": "₹250"}'

# Generate SSML
curl -X POST "http://localhost:8000/generate_ssml" \
  -H "Content-Type: application/json" \
  -d '{"locale": "hi-IN", "text": "₹250", "use_ssml": true}'

# Get supported locales
curl "http://localhost:8000/locales"
```

## Step 4: Run Tests

```bash
# Enter backend container
docker exec -it normalization-backend bash

# Run tests
python -m pytest tests/
```

## Troubleshooting

### Port Already in Use

If ports 3000 or 8000 are already in use:

1. Edit `docker-compose.yml`
2. Change port mappings:
   ```yaml
   ports:
     - "3001:80"  # Frontend
     - "8001:8000"  # Backend
   ```

### Container Won't Start

1. Check logs: `docker-compose logs`
2. Verify Docker is running: `docker ps`
3. Rebuild containers: `docker-compose up --build`

### Frontend Can't Connect to Backend

1. Check backend is running: `curl http://localhost:8000/health`
2. Verify CORS settings in `backend/main.py`
3. Check browser console for errors

## Next Steps

- Read the [README.md](README.md) for detailed documentation
- Check [examples/sample_queries.md](examples/sample_queries.md) for test cases
- Review [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for system design
- Add a new language following the guide in README.md

## Stopping the Application

```bash
docker-compose down
```

To also remove volumes:

```bash
docker-compose down -v
```
