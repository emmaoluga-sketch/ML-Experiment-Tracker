import React from 'react';

function ExperimentList({ experiments, onSelectExperiment, onDeleteExperiment, selectedId }) {
  return (
    <div className="experiment-list">
      {experiments.map((exp) => (
        <div
          key={exp.id}
          className={`experiment-card ${selectedId === exp.id ? 'selected' : ''}`}
          onClick={() => onSelectExperiment(exp)}
        >
          <div className="experiment-header">
            <h3>{exp.name}</h3>
            <span className="experiment-id">#{exp.id}</span>
          </div>
          
          <p className="experiment-date">
            {new Date(exp.created_at).toLocaleDateString()}
          </p>
          
          {exp.tags && exp.tags.length > 0 && (
            <div className="tags">
              {exp.tags.slice(0, 3).map((tag, idx) => (
                <span key={idx} className="tag-small">{tag}</span>
              ))}
              {exp.tags.length > 3 && <span className="tag-small">+{exp.tags.length - 3}</span>}
            </div>
          )}
          
          <div className="experiment-stats">
            {exp.metrics && Object.keys(exp.metrics).length > 0 && (
              <div className="stat">
                <span className="label">Metrics:</span>
                <span className="value">{Object.keys(exp.metrics).length}</span>
              </div>
            )}
            {exp.params && Object.keys(exp.params).length > 0 && (
              <div className="stat">
                <span className="label">Params:</span>
                <span className="value">{Object.keys(exp.params).length}</span>
              </div>
            )}
          </div>
          
          <button
            className="btn-delete"
            onClick={(e) => {
              e.stopPropagation();
              onDeleteExperiment(exp.id);
            }}
            title="Delete experiment"
          >
            🗑️
          </button>
        </div>
      ))}
    </div>
  );
}

export default ExperimentList;
