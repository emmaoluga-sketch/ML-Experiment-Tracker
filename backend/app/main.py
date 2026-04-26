"""FastAPI application for ML Experiment Tracker."""

import logging
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime

from . import models, database, schemas

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

# Initialize FastAPI app
app = FastAPI(
    title="ML Experiment Tracker",
    description="A lightweight MLOps tool for tracking machine learning experiments",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "ML Experiment Tracker API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/experiments", response_model=schemas.ExperimentResponse, status_code=201)
def create_experiment(
    experiment: schemas.ExperimentCreate,
    db: Session = Depends(database.get_db)
):
    """
    Create a new experiment.
    
    - **name**: Name of the experiment (required)
    - **params**: Dictionary of hyperparameters
    - **metrics**: Dictionary of performance metrics
    - **tags**: List of tags for organization
    - **artifacts**: Dictionary of artifact metadata
    - **notes**: Additional notes about the experiment
    """
    try:
        db_experiment = models.Experiment(**experiment.dict())
        db.add(db_experiment)
        db.commit()
        db.refresh(db_experiment)
        logger.info(f"Created experiment: {db_experiment.name} (ID: {db_experiment.id})")
        return db_experiment
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating experiment: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/experiments", response_model=List[schemas.ExperimentResponse])
def list_experiments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tags: Optional[str] = None,
    db: Session = Depends(database.get_db)
):
    """
    List all experiments with pagination.
    
    - **skip**: Number of experiments to skip (default: 0)
    - **limit**: Maximum number of experiments to return (default: 100, max: 1000)
    - **tags**: Filter by tags (comma-separated)
    """
    query = db.query(models.Experiment).order_by(desc(models.Experiment.created_at))
    
    if tags:
        tag_list = [t.strip() for t in tags.split(",")]
        query = query.filter(models.Experiment.tags.astext.contains(tag_list[0]))
    
    experiments = query.offset(skip).limit(limit).all()
    logger.info(f"Retrieved {len(experiments)} experiments")
    return experiments


@app.get("/experiments/{experiment_id}", response_model=schemas.ExperimentResponse)
def get_experiment(
    experiment_id: int,
    db: Session = Depends(database.get_db)
):
    """
    Get a specific experiment by ID.
    """
    experiment = db.query(models.Experiment).filter(
        models.Experiment.id == experiment_id
    ).first()
    
    if not experiment:
        logger.warning(f"Experiment not found: {experiment_id}")
        raise HTTPException(status_code=404, detail="Experiment not found")
    
    return experiment


@app.put("/experiments/{experiment_id}", response_model=schemas.ExperimentResponse)
def update_experiment(
    experiment_id: int,
    experiment: schemas.ExperimentUpdate,
    db: Session = Depends(database.get_db)
):
    """
    Update an existing experiment.
    """
    db_experiment = db.query(models.Experiment).filter(
        models.Experiment.id == experiment_id
    ).first()
    
    if not db_experiment:
        logger.warning(f"Experiment not found for update: {experiment_id}")
        raise HTTPException(status_code=404, detail="Experiment not found")
    
    try:
        update_data = experiment.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_experiment, key, value)
        
        db_experiment.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_experiment)
        logger.info(f"Updated experiment: {experiment_id}")
        return db_experiment
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating experiment: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/experiments/{experiment_id}", status_code=204)
def delete_experiment(
    experiment_id: int,
    db: Session = Depends(database.get_db)
):
    """
    Delete an experiment.
    """
    db_experiment = db.query(models.Experiment).filter(
        models.Experiment.id == experiment_id
    ).first()
    
    if not db_experiment:
        logger.warning(f"Experiment not found for deletion: {experiment_id}")
        raise HTTPException(status_code=404, detail="Experiment not found")
    
    try:
        db.delete(db_experiment)
        db.commit()
        logger.info(f"Deleted experiment: {experiment_id}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting experiment: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/experiments/stats/summary")
def get_summary(
    db: Session = Depends(database.get_db)
):
    """
    Get summary statistics of all experiments.
    """
    total = db.query(models.Experiment).count()
    return {
        "total_experiments": total,
        "recent_experiments": total,
        "timestamp": datetime.utcnow()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
