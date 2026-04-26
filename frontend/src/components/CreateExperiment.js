import React, { useState } from 'react';

function CreateExperiment({ onSubmit, onCancel }) {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    params: '{}',
    metrics: '{}',
    tags: '',
    notes: ''
  });
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError(null);

    try {
      // Validate required fields
      if (!formData.name.trim()) {
        setError('Experiment name is required');
        return;
      }

      // Parse JSON fields
      let params = {};
      let metrics = {};

      if (formData.params.trim()) {
        try {
          params = JSON.parse(formData.params);
        } catch (e) {
          setError('Invalid parameters JSON');
          return;
        }
      }

      if (formData.metrics.trim()) {
        try {
          metrics = JSON.parse(formData.metrics);
        } catch (e) {
          setError('Invalid metrics JSON');
          return;
        }
      }

      // Parse tags
      const tags = formData.tags
        .split(',')
        .map(tag => tag.trim())
        .filter(tag => tag.length > 0);

      // Submit
      onSubmit({
        name: formData.name,
        description: formData.description || null,
        params: params,
        metrics: metrics,
        tags: tags,
        notes: formData.notes || null
      });
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="create-experiment-form">
      <h2>Create New Experiment</h2>
      
      {error && <div className="form-error">❌ {error}</div>}
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Experiment Name *</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="e.g., xgboost-baseline"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="Describe your experiment..."
            rows="2"
          />
        </div>

        <div className="form-group">
          <label htmlFor="params">Parameters (JSON)</label>
          <textarea
            id="params"
            name="params"
            value={formData.params}
            onChange={handleChange}
            placeholder='{"learning_rate": 0.1, "batch_size": 32}'
            rows="3"
          />
        </div>

        <div className="form-group">
          <label htmlFor="metrics">Metrics (JSON)</label>
          <textarea
            id="metrics"
            name="metrics"
            value={formData.metrics}
            onChange={handleChange}
            placeholder='{"accuracy": 0.95, "f1": 0.92}'
            rows="3"
          />
        </div>

        <div className="form-group">
          <label htmlFor="tags">Tags (comma-separated)</label>
          <input
            type="text"
            id="tags"
            name="tags"
            value={formData.tags}
            onChange={handleChange}
            placeholder="baseline, v1, production"
          />
        </div>

        <div className="form-group">
          <label htmlFor="notes">Notes</label>
          <textarea
            id="notes"
            name="notes"
            value={formData.notes}
            onChange={handleChange}
            placeholder="Any additional notes about this experiment..."
            rows="3"
          />
        </div>

        <div className="form-actions">
          <button type="submit" className="btn btn-primary">Create Experiment</button>
          <button type="button" className="btn btn-secondary" onClick={onCancel}>Cancel</button>
        </div>
      </form>
    </div>
  );
}

export default CreateExperiment;
