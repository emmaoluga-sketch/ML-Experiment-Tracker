# Development Guide

## Project Structure

```
ml-experiment-tracker/
├── backend/          # FastAPI backend
├── cli/              # Command-line interface
├── frontend/         # React frontend
└── docs/             # Documentation
```

## Running the Project

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API will be available at: `http://127.0.0.1:8000`
API documentation: `http://127.0.0.1:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm start
```

Dashboard will be available at: `http://localhost:3000`

### CLI

```bash
cd cli
pip install -r requirements.txt
python tracker.py --help
```

## Database

The project uses SQLite by default. The database file is created automatically at:
- `backend/experiments.db`

### Reset Database

```bash
rm backend/experiments.db
```

The schema will be recreated on next API start.

## Testing

### Backend Tests

```bash
cd backend
pip install pytest pytest-asyncio
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Building for Production

### Backend

```bash
cd backend
pip install gunicorn
gunicorn app.main:app -w 4
```

### Frontend

```bash
cd frontend
npm run build
```

## Docker

### Build Images

```bash
docker-compose build
```

### Run with Docker Compose

```bash
docker-compose up -d
```

## Debugging

### Backend

- Use `--reload` flag for hot reload
- Add print statements or use debugger
- Check logs in terminal

### Frontend

- Use React Developer Tools browser extension
- Use `console.log()` for debugging
- Check browser console for errors

## Performance Optimization

- Use pagination for large datasets
- Index frequently queried columns
- Cache API responses on frontend
- Use lazy loading for components

## Security Considerations

- Add authentication to API
- Validate all user inputs
- Use HTTPS in production
- Implement rate limiting
- Store sensitive data securely

## Deployment

### Production Checklist

- [ ] Update environment variables
- [ ] Set up CORS properly
- [ ] Configure database for production
- [ ] Set up monitoring and logging
- [ ] Configure backups
- [ ] Test thoroughly
- [ ] Plan rollback strategy

## Common Issues

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### CORS Errors

Update `backend/app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Database Locked

```bash
# Ensure only one process accesses the database
killall python
```
