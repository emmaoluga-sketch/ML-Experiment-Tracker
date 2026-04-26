# ML Experiment Tracker

A lightweight MLOps tool for tracking machine learning experiments, hyperparameters, and results — without the overhead of heavy platforms.

## 🚀 Features

- **Track Experiments**: Log experiment runs via CLI with parameters and metrics
- **Store Everything**: Persist parameters, metrics, and artifacts locally
- **FastAPI Backend**: Modern, fast Python backend for serving data
- **SQLite Database**: Zero-config local database setup
- **React Dashboard**: Simple, intuitive UI for visualizing experiments
- **CLI Interface**: Command-line tool for quick experiment logging
- **Zero Dependencies**: Minimal external dependencies, run anywhere

## 🧠 Tech Stack

- **Backend**: Python, FastAPI, SQLAlchemy
- **Database**: SQLite
- **Frontend**: React, Axios
- **CLI**: Python argparse, requests

## 📋 Project Structure

```
ml-experiment-tracker/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── database.py
│   │   └── schemas.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── cli/
│   ├── __init__.py
│   ├── tracker.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js
│   │   ├── index.js
│   │   ├── components/
│   │   │   ├── ExperimentList.js
│   │   │   ├── ExperimentDetail.js
│   │   │   └── CreateExperiment.js
│   │   └── styles/
│   │       └── App.css
│   ├── package.json
│   └── Dockerfile
│
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── CONTRIBUTING.md
├── DEVELOPMENT.md
├── setup.py
└── requirements.txt
```

## ⚙️ Quick Start

### Prerequisites

- Python 3.8+
- Node.js 14+
- Docker & Docker Compose (optional)

### Backend Setup

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run the API server
uvicorn app.main:app --reload

# API will be available at http://127.0.0.1:8000
# API docs at http://127.0.0.1:8000/docs
```

### CLI Setup

```bash
# In a new terminal
cd cli
pip install -r requirements.txt

# Test the CLI
python tracker.py --help
```

### Frontend Setup

```bash
# In a new terminal
cd frontend
npm install
npm start

# Dashboard will be available at http://localhost:3000
```

## 🚀 Usage

### Log an Experiment via CLI

```bash
python tracker.py run \
  --name "xgboost-baseline" \
  --params '{"learning_rate": 0.1, "max_depth": 5}' \
  --metrics '{"accuracy": 0.92, "f1": 0.88}'
```

### Log with Tags

```bash
python tracker.py run \
  --name "neural-network-v2" \
  --params '{"epochs": 100, "batch_size": 32}' \
  --metrics '{"loss": 0.15, "accuracy": 0.95}' \
  --tags "deep-learning,production"
```

### View All Experiments

```bash
# Via CLI
python tracker.py list

# Via API
curl http://127.0.0.1:8000/experiments

# Via Dashboard
Open http://localhost:3000 in your browser
```

### Get Experiment Details

```bash
python tracker.py detail --id 1
```

### Delete an Experiment

```bash
python tracker.py delete --id 1
```

## 📊 API Endpoints

### Create Experiment

```http
POST /experiments
Content-Type: application/json

{
  "name": "experiment-name",
  "params": {"lr": 0.1, "batch_size": 32},
  "metrics": {"accuracy": 0.95, "loss": 0.15},
  "tags": ["baseline", "v1"]
}
```

### List All Experiments

```http
GET /experiments
```

### Get Single Experiment

```http
GET /experiments/{id}
```

### Update Experiment

```http
PUT /experiments/{id}
Content-Type: application/json

{
  "name": "updated-name",
  "params": {...},
  "metrics": {...}
}
```

### Delete Experiment

```http
DELETE /experiments/{id}
```

## 🐳 Docker Setup

### Run with Docker Compose

```bash
docker-compose up -d

# Services will be available at:
# Backend: http://127.0.0.1:8000
# Frontend: http://127.0.0.1:3000
```

### Build Specific Service

```bash
# Build backend
docker build -f backend/Dockerfile -t ml-tracker-backend ./backend

# Build frontend
docker build -f frontend/Dockerfile -t ml-tracker-frontend ./frontend
```

## 📁 File Structure Explained

### Backend

- **main.py**: FastAPI app with all endpoints
- **models.py**: SQLAlchemy ORM models for database
- **database.py**: Database connection and setup
- **schemas.py**: Pydantic request/response models

### CLI

- **tracker.py**: Command-line interface for experiment logging

### Frontend

- **App.js**: Main React component
- **ExperimentList.js**: Display all experiments
- **ExperimentDetail.js**: Show single experiment details
- **CreateExperiment.js**: Form to create new experiment

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Backend
DATABASE_URL=sqlite:///./experiments.db
FAST_API_HOST=127.0.0.1
FAST_API_PORT=8000
API_CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]

# Frontend
REACT_APP_API_URL=http://127.0.0.1:8000
```

### Database

The SQLite database is created automatically on first run at `backend/experiments.db`.

To reset the database:

```bash
rm backend/experiments.db
```

## 📈 Example Workflow

```bash
# 1. Start the backend
cd backend && uvicorn app.main:app --reload &

# 2. In another terminal, log experiments
cd cli
python tracker.py run --name "baseline" --params '{"lr":0.1}' --metrics '{"acc":0.85}'
python tracker.py run --name "v1" --params '{"lr":0.05}' --metrics '{"acc":0.92}'

# 3. View results via CLI
python tracker.py list

# 4. Start frontend (new terminal)
cd frontend && npm start

# 5. Open http://localhost:3000 to see dashboard
```

## 🚀 Scaling & Production

### Scale to PostgreSQL

Change `DATABASE_URL` in `backend/app/database.py`:

```python
DATABASE_URL = "postgresql://user:password@localhost/ml_tracker"
```

### Scale to S3/Cloud Storage

Update `models.py` to store artifacts:

```python
artifacts = Column(JSON)  # Store S3 paths
```

### Add Authentication

Implement JWT in `main.py`:

```python
from fastapi.security import HTTPBearer

security = HTTPBearer()
```

## 🐛 Troubleshooting

### Port 8000 Already in Use

```bash
uvicorn app.main:app --port 8001 --reload
```

### CORS Errors

Update `main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Database Locked

Ensure only one process is accessing the database:

```bash
killall python  # Kill all Python processes
```

## 📚 Future Enhancements

- [ ] Remote tracking server with authentication
- [ ] User authentication and team workspaces
- [ ] Artifact storage (S3, GCS)
- [ ] Advanced experiment comparison UI
- [ ] Hyperparameter search integration
- [ ] Real-time experiment monitoring
- [ ] Export experiments to CSV/JSON
- [ ] Webhook notifications
- [ ] Mobile app

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for development setup and guidelines.

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

## 💬 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Made with ❤️ for the ML community**