import React, { useState, useEffect } from 'react';

export default function NotificationPanel({ lastAlertQueryTimestamp }) {
  const [contacts, setContacts] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [newContactName, setNewContactName] = useState('');
  const [newContactPhone, setNewContactPhone] = useState('');
  const [newContactRel, setNewContactRel] = useState('Family');

  // Fetch contacts and notifications
  const fetchContacts = async () => {
    try {
      const response = await fetch('/api/contacts');
      if (response.ok) {
        const data = await response.json();
        setContacts(data);
      }
    } catch (e) {
      console.error("Failed to fetch contacts", e);
    }
  };

  const fetchNotifications = async () => {
    try {
      const response = await fetch('/api/notifications');
      if (response.ok) {
        const data = await response.json();
        setNotifications(data);
      }
    } catch (e) {
      console.error("Failed to fetch notifications", e);
    }
  };

  useEffect(() => {
    fetchContacts();
    fetchNotifications();
  }, [lastAlertQueryTimestamp]); // Refresh whenever a new query executes

  const handleAddContact = async (e) => {
    e.preventDefault();
    if (!newContactName.trim() || !newContactPhone.trim()) return;

    try {
      const response = await fetch('/api/contacts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: newContactName,
          phone: newContactPhone,
          relationship: newContactRel
        })
      });
      if (response.ok) {
        setNewContactName('');
        setNewContactPhone('');
        setNewContactRel('Family');
        fetchContacts();
      }
    } catch (err) {
      console.error("Error adding contact", err);
    }
  };

  const handleDeleteContact = async (id) => {
    try {
      const response = await fetch(`/api/contacts/${id}`, {
        method: 'DELETE'
      });
      if (response.ok) {
        fetchContacts();
      }
    } catch (err) {
      console.error("Error deleting contact", err);
    }
  };

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
      
      {/* Emergency Contacts Panel */}
      <div className="glass-panel" style={{ background: 'rgba(255,255,255,0.01)', border: '1px solid var(--border-color)', borderRadius: '10px' }}>
        <h4 style={{ fontFamily: 'var(--font-title)', fontSize: '1.05rem', color: 'white', marginBottom: '12px' }}>
          👥 Emergency Contact List
        </h4>

        {/* Add Contact Form */}
        <form onSubmit={handleAddContact} className="add-contact-form">
          <input 
            type="text" 
            placeholder="Name" 
            value={newContactName}
            onChange={(e) => setNewContactName(e.target.value)}
            required
          />
          <input 
            type="text" 
            placeholder="Phone/ID" 
            value={newContactPhone}
            onChange={(e) => setNewContactPhone(e.target.value)}
            required
          />
          <select 
            value={newContactRel}
            onChange={(e) => setNewContactRel(e.target.value)}
            style={{
              background: 'var(--bg-card-light)',
              color: 'white',
              border: '1px solid var(--border-color)',
              borderRadius: '6px',
              padding: '6px 8px',
              fontSize: '0.8rem',
              outline: 'none'
            }}
          >
            <option value="Family">Family</option>
            <option value="Friend">Friend</option>
            <option value="Doctor">Doctor</option>
            <option value="Authority Office">Authority Office</option>
          </select>
          <button type="submit">Add</button>
        </form>

        {/* Contacts List display */}
        <div className="contacts-list" style={{ maxHeight: '240px', overflowY: 'auto' }}>
          {contacts.length > 0 ? (
            contacts.map((c) => (
              <div key={c.id} className="contact-item" style={{ fontSize: '0.85rem' }}>
                <div>
                  <strong style={{ color: 'white' }}>{c.name}</strong> 
                  <span style={{ fontSize: '0.72rem', background: 'rgba(255,255,255,0.08)', padding: '2px 6px', borderRadius: '4px', marginLeft: '6px', color: 'var(--text-secondary)' }}>
                    {c.relationship}
                  </span>
                  <div style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', marginTop: '2px' }}>📞 {c.phone}</div>
                </div>
                <button 
                  onClick={() => handleDeleteContact(c.id)}
                  style={{
                    background: 'transparent',
                    border: 'none',
                    color: 'var(--alert-critical)',
                    cursor: 'pointer',
                    fontSize: '1rem',
                    padding: '4px'
                  }}
                  title="Remove contact"
                >
                  🗑️
                </button>
              </div>
            ))
          ) : (
            <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem', fontStyle: 'italic', padding: '10px' }}>
              No contacts registered. Add emergency contacts above.
            </div>
          )}
        </div>
      </div>

      {/* Dispatch Broadcast Log Panel */}
      <div className="glass-panel" style={{ background: 'rgba(255,255,255,0.01)', border: '1px solid var(--border-color)', borderRadius: '10px' }}>
        <h4 style={{ fontFamily: 'var(--font-title)', fontSize: '1.05rem', color: 'white', marginBottom: '12px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span>📢 Notification Dispatch Log</span>
          <button 
            onClick={fetchNotifications}
            style={{ background: 'transparent', border: 'none', color: 'var(--alert-low)', cursor: 'pointer', fontSize: '0.8rem' }}
          >
            🔄 Refresh
          </button>
        </h4>

        <div style={{ maxHeight: '280px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {notifications.length > 0 ? (
            notifications.map((n) => (
              <div key={n.id} style={{
                background: 'rgba(255,255,255,0.02)',
                border: '1px solid var(--border-color)',
                borderRadius: '6px',
                padding: '10px',
                fontSize: '0.8rem'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                  <strong style={{ color: 'white' }}>Alert Sent To: {n.contact_name} ({n.contact_phone})</strong>
                  <span style={{ 
                    color: n.status === 'Sent' ? 'var(--alert-safe)' : 'var(--alert-critical)',
                    fontWeight: 'bold',
                    fontSize: '0.75rem'
                  }}>
                    ● {n.status}
                  </span>
                </div>
                <div style={{ color: 'var(--text-secondary)', fontStyle: 'italic', fontFamily: 'monospace', fontSize: '0.78rem', background: '#0a0d14', padding: '6px', borderRadius: '4px', margin: '4px 0' }}>
                  {n.message}
                </div>
                <div style={{ color: 'var(--text-muted)', fontSize: '0.7rem', textAlign: 'right' }}>
                  Timestamp: {new Date(n.timestamp).toLocaleTimeString()}
                </div>
              </div>
            ))
          ) : (
            <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem', fontStyle: 'italic', padding: '10px' }}>
              Dispatch log empty. Report an active emergency alert to trigger automated contact notifications.
            </div>
          )}
        </div>
      </div>

    </div>
  );
}
