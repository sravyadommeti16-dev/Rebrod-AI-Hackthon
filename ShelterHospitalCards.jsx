import React from 'react';

export default function ShelterHospitalCards({ shelters, hospitals, resources }) {
  const hasShelters = shelters && shelters.length > 0;
  const hasHospitals = hospitals && hospitals.length > 0;
  const hasResources = resources && resources.length > 0;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      
      {/* Shelters & Camps Directory */}
      <div>
        <h4 style={{ fontFamily: 'var(--font-title)', fontSize: '1.05rem', color: '#10b981', marginBottom: '10px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span>⛺ Recommended Relief Camps (Safe Havens)</span>
        </h4>
        {hasShelters ? (
          <div className="cards-grid">
            {shelters.map((shelter, idx) => {
              const isNearCap = shelter.occupancy.includes('Capacity') || parseInt(shelter.occupancy.split('/')[0]) > 250;
              const badgeClass = isNearCap ? 'card-badge high' : 'card-badge safe';
              
              return (
                <div key={idx} className="facility-card">
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <h4>{shelter.name}</h4>
                    <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{shelter.distance}</span>
                  </div>
                  <span className={badgeClass}>{shelter.status}</span>
                  <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '6px' }}>
                    📍 {shelter.location}
                  </p>
                  <p style={{ fontSize: '0.85rem', color: 'white', marginBottom: '8px' }}>
                    📊 Occupancy: <strong>{shelter.occupancy}</strong>
                  </p>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px', marginBottom: '8px' }}>
                    {shelter.supplies.map((supply, sIdx) => (
                      <span key={sIdx} style={{ fontSize: '0.72rem', background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '4px', padding: '1px 6px' }}>
                        {supply}
                      </span>
                    ))}
                  </div>
                  <p style={{ fontSize: '0.8rem', color: 'var(--alert-low)', fontWeight: '600' }}>
                    📞 Call: {shelter.phone}
                  </p>
                </div>
              );
            })}
          </div>
        ) : (
          <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem', fontStyle: 'italic', padding: '10px', background: 'rgba(255,255,255,0.01)', border: '1px dashed var(--border-color)', borderRadius: '6px' }}>
            No shelters recommended yet. Report an active emergency to load nearest relief camps.
          </div>
        )}
      </div>

      {/* Medical Facilities Directory */}
      <div>
        <h4 style={{ fontFamily: 'var(--font-title)', fontSize: '1.05rem', color: '#ef4444', marginBottom: '10px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span>🏥 Emergency Medical Care & Hospital Finder</span>
        </h4>
        {hasHospitals ? (
          <div className="cards-grid">
            {hospitals.map((hosp, idx) => {
              const noBeds = hosp.icu_beds.toLowerCase().includes('0') || hosp.icu_beds.toLowerCase().includes('high');
              const badgeClass = noBeds ? 'card-badge high' : 'card-badge safe';
              
              return (
                <div key={idx} className="facility-card">
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <h4>{hosp.name}</h4>
                    <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{hosp.distance}</span>
                  </div>
                  <span className={badgeClass}>{hosp.status}</span>
                  <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '6px' }}>
                    📍 {hosp.location}
                  </p>
                  <p style={{ fontSize: '0.85rem', color: 'white', marginBottom: '8px' }}>
                    🛏️ ICU Beds: <strong style={{ color: noBeds ? 'var(--alert-high)' : 'var(--alert-safe)' }}>{hosp.icu_beds}</strong>
                  </p>
                  <p style={{ fontSize: '0.85rem', color: 'white', marginBottom: '8px' }}>
                    💨 Oxygen Supply: <strong style={{ color: 'var(--alert-safe)' }}>{hosp.oxygen_status}</strong>
                  </p>
                  <p style={{ fontSize: '0.8rem', color: 'var(--alert-low)', fontWeight: '600' }}>
                    📞 Emergency Desk: {hosp.phone}
                  </p>
                </div>
              );
            })}
          </div>
        ) : (
          <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem', fontStyle: 'italic', padding: '10px', background: 'rgba(255,255,255,0.01)', border: '1px dashed var(--border-color)', borderRadius: '6px' }}>
            No medical centers recommended yet. Report an active emergency to locate nearest open trauma clinics.
          </div>
        )}
      </div>

      {/* Emergency Resources Cache */}
      <div>
        <h4 style={{ fontFamily: 'var(--font-title)', fontSize: '1.05rem', color: '#f97316', marginBottom: '10px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span>📦 Resource Stockpile Depots</span>
        </h4>
        {hasResources ? (
          <div className="cards-grid">
            {resources.map((hub, idx) => (
              <div key={idx} className="facility-card" style={{ borderLeft: '3px solid var(--alert-high)' }}>
                <h4>{hub.hub_name}</h4>
                <span className="card-badge safe" style={{ background: 'rgba(249, 115, 22, 0.15)', color: 'var(--alert-high)', border: '1px solid rgba(249, 115, 22, 0.3)' }}>
                  {hub.status}
                </span>
                <div style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginTop: '8px', display: 'flex', flexDirection: 'column', gap: '3px' }}>
                  <span>🍞 Rations: <strong>{hub.food_packets}</strong></span>
                  <span>💧 Clean Water: <strong>{hub.water_liters}</strong></span>
                  <span>🩹 First Aid Kits: <strong>{hub.first_aid_kits}</strong></span>
                  {hub.dry_clothes && <span>👕 Dry Clothes: <strong>{hub.dry_clothes}</strong></span>}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem', fontStyle: 'italic', padding: '10px', background: 'rgba(255,255,255,0.01)', border: '1px dashed var(--border-color)', borderRadius: '6px' }}>
            No supply hubs cached. Reports of specific resource needs will list local distribution hubs.
          </div>
        )}
      </div>

    </div>
  );
}
