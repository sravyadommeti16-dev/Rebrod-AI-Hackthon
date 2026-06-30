import React, { useState, useEffect, useRef } from 'react';

const QUICK_ACTIONS = [
  { text: "🌊 Chennai Flood", query: "We are trapped by severe flooding in Chennai Central area, water level is rising. Send help!" },
  { text: "🌀 Mumbai Cyclone", query: "Heavy cyclone winds and tree falls near Bandra West Mumbai. Power lines are broken." },
  { text: "⛰️ Uttarakhand Landslide", query: "Landslide and heavy mudflow blocking Rajpur road in Uttarakhand. Boulders rolling down." }
];

export default function ChatAssistant({ onReportResponse, onProcessingChange, processing }) {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: "👋 Welcome to Sentinel AI Emergency Command Copilot. Tell me what emergency you are facing (type or use the mic button for voice reporting)." }
  ]);
  const [inputQuery, setInputQuery] = useState('');
  const [selectedLang, setSelectedLang] = useState('en');
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef(null);
  const messagesEndRef = useRef(null);

  // Auto scroll to bottom of chat
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Set up Speech Recognition on mount
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const rec = new SpeechRecognition();
      rec.continuous = false;
      rec.interimResults = false;
      rec.lang = 'en-IN'; // Indian English pronunciation optimization
      
      rec.onstart = () => setIsListening(true);
      rec.onend = () => setIsListening(false);
      
      rec.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInputQuery(transcript);
        setMessages(prev => [...prev, { sender: 'bot', text: `🎙️ Transcribed Voice: "${transcript}"` }]);
      };
      
      rec.onerror = (e) => {
        console.error(e);
        setIsListening(false);
      };
      
      recognitionRef.current = rec;
    }
  }, []);

  const toggleListening = () => {
    if (!recognitionRef.current) {
      alert("Voice recognition is not supported in this browser. Please use Google Chrome or Microsoft Edge.");
      return;
    }
    if (isListening) {
      recognitionRef.current.stop();
    } else {
      recognitionRef.current.start();
    }
  };

  const handleSend = async (queryText = inputQuery) => {
    if (!queryText.trim()) return;
    
    // Append user message
    setMessages(prev => [...prev, { sender: 'user', text: queryText }]);
    setInputQuery('');
    onProcessingChange(true);

    try {
      const response = await fetch('/api/disaster/report', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: queryText,
          language: selectedLang
        })
      });

      if (response.ok) {
        const data = await response.json();
        onReportResponse(data);
        
        // Append response plan based on selected language
        const responseText = selectedLang !== 'en' && data.translated_plan 
          ? data.translated_plan 
          : data.final_response;
          
        setMessages(prev => [...prev, { sender: 'bot', text: responseText }]);
      } else {
        const errText = await response.text();
        setMessages(prev => [...prev, { sender: 'bot', text: `❌ Error running orchestrator: ${errText}`, error: true }]);
      }
    } catch (err) {
      setMessages(prev => [...prev, { sender: 'bot', text: `❌ Network connection failed: ${err.message}`, error: true }]);
    } finally {
      onProcessingChange(false);
    }
  };

  return (
    <div className="glass-panel chat-panel" style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px', borderBottom: '1px solid var(--border-color)', paddingBottom: '8px' }}>
        <h3 style={{ fontFamily: 'var(--font-title)', fontSize: '1.2rem', color: 'white' }}>🚨 Emergency Copilot</h3>
        <select 
          value={selectedLang}
          onChange={(e) => setSelectedLang(e.target.value)}
          style={{
            background: 'var(--bg-card-light)',
            color: 'white',
            border: '1px solid var(--border-color)',
            borderRadius: '4px',
            padding: '4px 8px',
            fontSize: '0.8rem',
            outline: 'none',
            cursor: 'pointer'
          }}
        >
          <option value="en">English (EN)</option>
          <option value="hi">हिन्दी (Hindi)</option>
          <option value="ta">தமிழ் (Tamil)</option>
          <option value="te">తెలుగు (Telugu)</option>
        </select>
      </div>

      {/* Chat Bubble History */}
      <div className="chat-messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message-bubble ${msg.sender} ${msg.error ? 'error' : ''}`}>
            {msg.text.split('\n').map((line, i) => (
              <React.Fragment key={i}>
                {line}
                <br />
              </React.Fragment>
            ))}
          </div>
        ))}
        {processing && (
          <div className="message-bubble bot" style={{ fontStyle: 'italic', color: 'var(--text-secondary)' }}>
            ⚙️ Orchestrator linking nodes: [DET] ➜ [RAG] ➜ [RTE] ➜ [FAC] ➜ [NOT] ➜ [TRN]...
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Prompts Helper */}
      <div className="quick-prompts">
        {QUICK_ACTIONS.map((action, idx) => (
          <button
            key={idx}
            className="quick-prompt-btn"
            onClick={() => handleSend(action.query)}
            disabled={processing}
          >
            {action.text}
          </button>
        ))}
      </div>

      {/* Input Bar */}
      <div className="chat-input-container">
        <input
          type="text"
          placeholder="Describe your emergency..."
          value={inputQuery}
          onChange={(e) => setInputQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          disabled={processing}
        />
        <button 
          className={`icon-btn ${isListening ? 'voice-active' : ''}`}
          onClick={toggleListening}
          disabled={processing}
          title="Voice reporting"
        >
          <svg style={{ width: '20px', height: '20px' }} viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.3-3c0 3-2.54 5.1-5.3 5.1S6.7 14 6.7 11H5c0 3.41 2.72 6.23 6 6.72V21h2v-3.28c3.28-.48 6-3.3 6-6.72h-1.7z"/>
          </svg>
        </button>
        <button 
          className="send-btn"
          onClick={() => handleSend()}
          disabled={processing || !inputQuery.trim()}
          title="Send Report"
        >
          <svg style={{ width: '18px', height: '18px' }} viewBox="0 0 24 24" fill="currentColor">
            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
          </svg>
        </button>
      </div>
    </div>
  );
}
