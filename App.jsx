import React, { useState } from 'react';
import LiveStatus from './components/LiveStatus';
import ChatAssistant from './components/ChatAssistant';
import AgentWorkflowVisualizer from './components/AgentWorkflowVisualizer';
import InteractiveMap from './components/InteractiveMap';
import ShelterHospitalCards from './components/ShelterHospitalCards';
import NotificationPanel from './components/NotificationPanel';

export default function App() {
  const [processing, setProcessing] = useState(false);
  const [activeTab, setActiveTab] = useState('map');
  const [lastQueryTime, setLastQueryTime] = useState(null);
  
  // Disaster Global States
  const [activeAlert, setActiveAlert] = useState({
    disasterType: 'none',
    severity: 'normal',
    location: 'Unknown'
  });
  
  const [routes, setRoutes] = useState([]);
  const [blockedZones, setBlockedZones] = useState([]);
  const [mapCenter, setMapCenter] = useState([13.0827, 80.2707]); // Default Chennai Central
  const [shelters, setShelters] = useState([]);
  const [hospitals, setHospitals] = useState([]);
  const [resources, setResources] = useState([]);
  const [executionSteps, setExecutionSteps] = useState([]);

  // Handles state payload update from the multi-agent backend output
  const handleReportResponse = (data) => {
    setActiveAlert({
      disasterType: data.disaster_type,
      severity: data.severity,
      location: data.location
    });
    setRoutes(data.routes || []);
    setBlockedZones(data.blocked_zones || []);
    setMapCenter(data.map_center || [13.0827, 80.2707]);
    setShelters(data.shelters || []);
    setHospitals(data.hospitals || []);
    setResources(data.resources || []);
    setExecutionSteps(data.execution_steps || []);
    setLastQueryTime(Date.now());
    
    // Automatically switch tabs to highlight relevant content
    if (data.routes && data.routes.length > 0) {
      setActiveTab('map');
    } else {
      setActiveTab('facilities');
    }
  };

  return (
    <div className="app-container">
      {/* Premium Dashboard Header */}
      <header className="app-header glass-panel" style={{ padding: '12px 20px', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
        <div className="header-brand">
          {/* SVG emergency pulse icon */}
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
          </svg>
          <div>
            <h1 style={{ margin: 0, fontSize: '1.45rem' }}>SENTINEL AI</h1>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', letterSpacing: '0.5px' }}>
              MULTI-AGENT EMERGENCY RESPONSE COPILOT
            </div>
          </div>
        </div>
        <div className="header-meta">
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem', background: 'rgba(255,255,255,0.04)', padding: '6px 12px', borderRadius: '20px', border: '1px solid var(--border-color)' }}>
            <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#34c759', boxShadow: '0 0 8px #34c759' }} />
            <span>Telemetry: Core Network Active</span>
          </div>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>V1.0 (Hackathon Release)</span>
        </div>
      </header>

      {/* Warning Ticker alert panel */}
      <LiveStatus activeAlert={activeAlert} />

      {/* Content Layout Grid */}
      <div className="dashboard-grid">
        
        {/* Left Side: Conversational Assist Panel */}
        <section className="chat-panel">
          <ChatAssistant 
            onReportResponse={handleReportResponse} 
            onProcessingChange={setProcessing}
            processing={processing}
          />
        </section>

        {/* Right Side: Command Center Panels */}
        <section className="content-panel" style={{ minHeight: 0 }}>
          
          {/* Real-time Multi-Agent process visualizer */}
          <AgentWorkflowVisualizer 
            executionSteps={executionSteps} 
            processing={processing}
          />

          {/* Navigation tabs for map/shelters/alerts */}
          <div className="glass-panel" style={{ flexGrow: 1, display: 'flex', flexDirection: 'column', minHeight: 0, padding: '16px 20px' }}>
            <nav className="tabs-navigation" style={{ marginBottom: '12px' }}>
              <button 
                className={`tab-btn ${activeTab === 'map' ? 'active' : ''}`}
                onClick={() => setActiveTab('map')}
              >
                🗺️ Evacuation Route Map
              </button>
              <button 
                className={`tab-btn ${activeTab === 'facilities' ? 'active' : ''}`}
                onClick={() => setActiveTab('facilities')}
              >
                ⛺ Shelters & Hospitals
              </button>
              <button 
                className={`tab-btn ${activeTab === 'notifications' ? 'active' : ''}`}
                onClick={() => setActiveTab('notifications')}
              >
                📢 Contacts & Broadcasts
              </button>
            </nav>

            <div className="tab-content" style={{ flexGrow: 1, overflowY: 'auto' }}>
              {activeTab === 'map' && (
                <InteractiveMap 
                  routes={routes} 
                  blockedZones={blockedZones} 
                  center={mapCenter}
                  shelters={shelters}
                  hospitals={hospitals}
                />
              )}
              
              {activeTab === 'facilities' && (
                <ShelterHospitalCards 
                  shelters={shelters} 
                  hospitals={hospitals}
                  resources={resources}
                />
              )}

              {activeTab === 'notifications' && (
                <NotificationPanel 
                  lastAlertQueryTimestamp={lastQueryTime}
                />
              )}
            </div>
          </div>

        </section>
      </div>
    </div>
  );
}
