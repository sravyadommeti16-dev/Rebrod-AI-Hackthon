import React, { useState } from 'react';

const AGENT_NODES = [
  { id: 'orc', label: 'ORC', name: 'Orchestrator Agent', desc: 'Routes flow and aggregates multi-agent outputs' },
  { id: 'det', label: 'DET', name: 'Detection Agent', desc: 'Classifies disaster category, severity & language' },
  { id: 'rag', label: 'RAG', name: 'RAG Agent', desc: 'Retrieves safety instructions from vector store' },
  { id: 'rte', label: 'RTE', name: 'Route Agent', desc: 'Plans safe evacuation routes around hazard red zones' },
  { id: 'fac', label: 'FAC', name: 'Facility Agent', desc: 'Identifies open shelters & hospital ICU beds' },
  { id: 'not', label: 'NOT', name: 'Notification Agent', desc: 'Formulates contact notification SMS alerts' },
  { id: 'trn', label: 'TRN', name: 'Translation Agent', desc: 'Translates plans into regional Indian languages' }
];

export default function AgentWorkflowVisualizer({ executionSteps, processing }) {
  const [selectedNode, setSelectedNode] = useState(null);

  // Determine completed and active nodes based on backend log messages
  const getStatus = (nodeId) => {
    if (processing) {
      // Simulate status during load
      if (executionSteps.length === 0) return nodeId === 'orc' ? 'active' : 'idle';
      
      const lastLine = executionSteps[executionSteps.length - 1].toLowerCase();
      if (nodeId === 'orc') return 'completed';
      if (nodeId === 'det') return lastLine.includes('classified') ? 'completed' : (lastLine.includes('initiated') ? 'active' : 'idle');
      if (nodeId === 'rag') return lastLine.includes('retrieved') ? 'completed' : (executionSteps.some(s => s.toLowerCase().includes('classified')) ? 'active' : 'idle');
      if (nodeId === 'rte') return lastLine.includes('calculated') ? 'completed' : (executionSteps.some(s => s.toLowerCase().includes('retrieved')) ? 'active' : 'idle');
      if (nodeId === 'fac') return lastLine.includes('allocated') || lastLine.includes('identified') ? 'completed' : (executionSteps.some(s => s.toLowerCase().includes('calculated')) ? 'active' : 'idle');
      if (nodeId === 'not') return lastLine.includes('prepared broadcast') ? 'completed' : (executionSteps.some(s => s.toLowerCase().includes('allocated')) ? 'active' : 'idle');
      if (nodeId === 'trn') return lastLine.includes('translated') ? 'completed' : (executionSteps.some(s => s.toLowerCase().includes('prepared broadcast')) ? 'active' : 'idle');
      return 'idle';
    }
    
    // Static display when done
    if (executionSteps && executionSteps.length > 0) {
      return 'completed';
    }
    return 'idle';
  };

  return (
    <div className="glass-panel agent-flow-container">
      <h3 style={{ fontFamily: 'var(--font-title)', fontSize: '1.15rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span>🤖 Multi-Agent Brain Orchestration</span>
        {processing && <span style={{ fontSize: '0.8rem', color: 'var(--alert-low)', animation: 'blink 0.8s infinite alternate' }}>● Orchestrating...</span>}
      </h3>
      <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
        Click on any agent node below to inspect its sub-agent profile.
      </p>

      {/* Horizontal workflow timeline diagram */}
      <div className="agent-timeline">
        {AGENT_NODES.map((node) => {
          const status = getStatus(node.id);
          let nodeClass = 'agent-node';
          if (status === 'active') nodeClass += ' active';
          if (status === 'completed') nodeClass += ' completed';

          return (
            <div 
              key={node.id} 
              className={nodeClass}
              onClick={() => setSelectedNode(node)}
            >
              {node.label}
              <div className="node-tooltip">
                <strong>{node.name}</strong>
              </div>
            </div>
          );
        })}
      </div>

      {/* Selected Node Inspector Panel */}
      {selectedNode && (
        <div style={{
          background: 'rgba(255, 255, 255, 0.03)',
          border: '1px dashed var(--border-color)',
          borderRadius: '8px',
          padding: '10px 14px',
          fontSize: '0.82rem',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <div>
            <strong style={{ color: 'white' }}>{selectedNode.name}:</strong>
            <span style={{ color: 'var(--text-secondary)', marginLeft: '6px' }}>{selectedNode.desc}</span>
          </div>
          <button 
            onClick={() => setSelectedNode(null)}
            style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', fontSize: '0.8rem' }}
          >
            ✕
          </button>
        </div>
      )}

      {/* Raw Thinking Logs Console */}
      <div className="execution-logs-box">
        <div style={{ color: 'var(--text-muted)', fontSize: '0.75rem', marginBottom: '8px', borderBottom: '1px solid rgba(255,255,255,0.05)', paddingBottom: '4px' }}>
          SENTINEL COORDINATION LOGS & CONSOLE PIPELINE
        </div>
        {executionSteps && executionSteps.length > 0 ? (
          executionSteps.map((step, idx) => {
            const isOrchestrator = step.includes('Orchestrator') || step.includes('initiated');
            const isCompleted = step.includes('complete') || step.includes('Dispatching');
            let lineClass = 'log-line';
            if (isOrchestrator) lineClass += ' orchestrator';
            if (isCompleted) lineClass += ' completed';
            
            return (
              <div key={idx} className={lineClass}>
                {step}
              </div>
            );
          })
        ) : (
          <div style={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>
            Console idle. Send a message to report an emergency.
          </div>
        )}
      </div>
    </div>
  );
}
