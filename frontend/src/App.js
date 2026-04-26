import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ExperimentList from './components/ExperimentList';
import CreateExperiment from './components/CreateExperiment';
import './styles/App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

function App() {
  const [experiments, setExperiments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [selectedExperiment, setSelectedExperiment] = useState(null);

  // Fetch experiments
  const fetchExperiments = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_URL}/experiments`);
      setExperiments(response.data);
      setError(null);
    } catch (err) {
      setError(`Failed to fetch experiments: ${err.message}`);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Initial load
  useEffect(() => {
    fetchExperiments();
  }, []);

  // Handle creating experiment
  const handleCreateExperiment = async (experimentData) => {
    try {
      const response = await axios.post(`${API_URL}/experiments`, experimentData);
      setExperiments([response.data, ...experiments]);
      setShowCreateForm(false);
      setError(null);
    } catch (err) {
      setError(`Failed to create experiment: ${err.message}`);
      console.error(err);
    }
  };

  // Handle deleting experiment
  const handleDeleteExperiment = async (id) => {
    if (window.confirm('Are you sure you want to delete this experiment?')) {
      try {
        await axios.delete(`${API_URL}/experiments/${id}`);
        setExperiments(experiments.filter(exp => exp.id !== id));
        setSelectedExperiment(null);
        setError(null);
      } catch (err) {
        setError(`Failed to delete experiment: ${err.message}`);
        console.error(err);
      }
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🧪 ML Experiment Tracker</h1>
        <p>Track and manage your machine learning experiments</p>
      </header>

      <div className="app-container">
        {error && (
          <div className="error-message">
            <span>❌ {error}</span>
            <button onClick={() => setError(null)}>Dismiss</button>
          </div>
        )}

        <div className="controls">
          <button
            className="btn btn-primary"
            onClick={() => setShowCreateForm(!showCreateForm)}
          >
            {showCreateForm ? 'Cancel' : '➕ New Experiment'}
          </button>
          <button
            className="btn btn-secondary"
            onClick={fetchExperiments}
            disabled={loading}
          >
            {loading ? 'Refreshing...' : '🔄 Refresh'}
          </button>
        </div>

        {showCreateForm && (
          <CreateExperiment
            onSubmit={handleCreateExperiment}
            onCancel={() => setShowCreateForm(false)}
          />
        )}

        <div className="content">
          <div className="experiments-section">
            <h2>Experiments ({experiments.length})</h2>
            {loading && <p className="loading">Loading experiments...</p>}
            {!loading && experiments.length === 0 && (
              <p className="empty-state">No experiments yet. Create one to get started!</p>
            )}
            {!loading && experiments.length > 0 && (
              <ExperimentList
                experiments={experiments}
                onSelectExperiment={setSelectedExperiment}
                onDeleteExperiment={handleDeleteExperiment}
                selectedId={selectedExperiment?.id}
              />
            )}
          </div>

          {selectedExperiment && (
            <div className="detail-section">
              <h2>Experiment Details</h2>
              <div className="experiment-detail">
                <h3>{selectedExperiment.name}</h3>
                <p className="experiment-id">ID: {selectedExperiment.id}</p>
                {selectedExperiment.description && (
                  <p className="description">{selectedExperiment.description}</p>
                )}

                {selectedExperiment.tags && selectedExperiment.tags.length > 0 && (
                  <div className="tags">
                    {selectedExperiment.tags.map((tag, idx) => (
                      <span key={idx} className="tag">
                        {tag}
                      </span>
                    ))}
                  </div>
                )}

                {selectedExperiment.params && Object.keys(selectedExperiment.params).length > 0 && (
                  <div className="section">
                    <h4>Parameters</h4>
                    <pre>{JSON.stringify(selectedExperiment.params, null, 2)}</pre>
                  </div>
                )}

                {selectedExperiment.metrics && Object.keys(selectedExperiment.metrics).length > 0 && (
                  <div className="section">
                    <h4>Metrics</h4>
                    <pre>{JSON.stringify(selectedExperiment.metrics, null, 2)}</pre>
                  </div>
                )}

                {selectedExperiment.notes && (
                  <div className="section">
                    <h4>Notes</h4>
                    <p>{selectedExperiment.notes}</p>
                  </div>
                )}

                <p className="timestamp">
                  Created: {new Date(selectedExperiment.created_at).toLocaleString()}
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
