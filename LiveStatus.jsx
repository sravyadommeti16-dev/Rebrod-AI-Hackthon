import React from 'react';

export default function LiveStatus({ activeAlert }) {
  const { disasterType, severity, location } = activeAlert || {};
  
  const isEmergency = disasterType && disasterType !== 'none';
  const displaySeverity = severity ? severity.toUpperCase() : 'NORMAL';
  
  let bannerClass = 'live-status-bar ';
  let textInfo = 'All Systems Operational. Monitoring active weather alerts...';
  
  if (isEmergency) {
    if (severity === 'critical') {
      bannerClass += 'critical-alert';
      textInfo = `🚨 DANGER: ACTIVE CRITICAL ${disasterType.toUpperCase()} DETECTED IN ${location.toUpperCase()}. EVACUATION PROTOCOLS IN PROGRESS.`;
    } else if (severity === 'high') {
      bannerClass += 'high-alert';
      textInfo = `⚠️ WARNING: HIGH SEVERITY ${disasterType.toUpperCase()} DETECTED IN ${location.toUpperCase()}. GET READY TO EVACUATE.`;
    } else {
      bannerClass += 'medium-alert';
      textInfo = `ℹ️ NOTICE: ${disasterType.toUpperCase()} ALERT IN ${location.toUpperCase()}. STAY INDOORS AND LISTEN TO AUTHORITIES.`;
    }
  }

  return (
    <div className={bannerClass} style={{
      display: 'flex',
      alignItems: 'center',
      gap: '12px',
      padding: '10px 16px',
      borderRadius: '8px',
      background: isEmergency ? 'rgba(239, 68, 68, 0.15)' : 'rgba(16, 185, 129, 0.1)',
      border: `1px solid ${isEmergency ? 'rgba(239, 68, 68, 0.3)' : 'rgba(16, 185, 129, 0.2)'}`,
      transition: 'all 0.3s ease'
    }}>
      <div className="live-status-indicator" style={{
        width: '10px',
        height: '10px',
        borderRadius: '50%',
        background: isEmergency ? '#ef4444' : '#10b981',
        boxShadow: isEmergency ? '0 0 10px #ef4444' : '0 0 10px #10b981',
        animation: 'blink 1s infinite alternate'
      }} />
      <span style={{ fontSize: '0.85rem', fontWeight: '600', color: isEmergency ? '#ef4444' : '#10b981', minWidth: '80px' }}>
        [{displaySeverity}]
      </span>
      <marquee style={{ fontSize: '0.85rem', color: '#f3f4f6', flexGrow: 1 }} scrollamount="4">
        {textInfo}
      </marquee>
      {isEmergency && (
        <span style={{ fontSize: '0.8rem', background: 'rgba(255,255,255,0.08)', padding: '2px 8px', borderRadius: '4px', color: '#9ca3af' }}>
          Loc: {location}
        </span>
      )}
    </div>
  );
}
