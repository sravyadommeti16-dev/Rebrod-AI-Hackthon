# Sentinel AI: Multi-Agent Disaster Response Copilot

> 🏆 Built for **Challenge 1 – Build an AI System** under the theme of AI-Native Emergency Response.

Sentinel AI is a production-ready emergency coordination command center designed to assist victims and responders during natural disasters (floods, cyclones, earthquakes, landslides, and fires). Rather than functioning as a standard conversational chatbot, Sentinel AI coordinates **eight specialized AI agents** under a central **Decision Orchestrator** to diagnose emergencies, pull safety protocols (RAG), calculate safe evacuation routes, allocate shelter beds, coordinate stockpiles, translate plans, and dispatch emergency SMS notifications.

---

## 📸 Mockups & Dashboard Features

Sentinel AI's user interface is styled like a modern Emergency Operations Command Center (glassmorphism, dark theme, and color-coded danger telemetry indicators):
1. **Emergency Chat Assistant**: Supports natural text queries and voice reporting (utilizing Chrome/Edge HTML5 Web Speech APIs).
2. **Interactive Disaster Map**: Powered by Leaflet, displaying live coordinate pins, red warning zones (e.g., flooded rivers or landslides), and green safe passage lines.
3. **Multi-Agent Orchestration Console**: Shows a live state diagram illuminating agent execution nodes (`DET ➜ RAG ➜ RTE ➜ FAC ➜ NOT ➜ TRN`) along with raw console reasoning steps.
4. **Relief & Medical Directory**: Interactive cards tracking occupancy, doctor availability, oxygen supplies, and critical bed capacities.
5. **SMS Notification Dispatch**: Registers emergency contacts and lists outgoing text messages dispatched to family members or responders.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.7+, FastAPI, SQLAlchemy, SQLite (PostgreSQL compatible), Requests, Scikit-learn (TF-IDF Cosine Similarity vector matching), Pydantic.
- **Frontend**: React 18, Vite, Leaflet.js Mapping Engine, Vanilla CSS.
- **LLM Integration**: Google Gemini 1.5 Flash (via direct HTTP interface) with automatic **Demo Mode (Mock Fallback)** when no API key is present.

---

## 📂 Project Structure

```
sentinel-ai/
├── backend/
│   ├── app/
│   │   ├── agents/            # Specialized Multi-Agent logic
│   │   │   ├── detection.py   # Disaster parameters & severity detection
│   │   │   ├── hospital.py    # Emergency clinic beds finder
│   │   │   ├── notification.py# Notification text formatter
│   │   │   ├── orchestrator.py# Main state coordinator
│   │   │   ├── rag.py         # Vector similarity search dispatcher
│   │   │   ├── resource.py    # Resource cache stockpile coordinator
│   │   │   ├── route.py       # Safe evacuation coordinates builder
│   │   │   ├── shelter.py     # Relief camps occupancy checker
│   │   │   └── translation.py # Multi-lingual translator
│   │   ├── models/
│   │   │   ├── models.py      # SQLAlchemy DB models
│   │   │   └── schemas.py     # Pydantic validation schemas
│   │   ├── utils/
│   │   │   ├── gemini_client.py # Gemini connection wrapper & Mock mode
│   │   │   └── rag_store.py   # Cosine similarity vector guideline store
│   │   ├── config.py          # App settings & environment loads
│   │   ├── database.py        # SQLite engine definitions
│   │   └── main.py            # FastAPI main router & database seeders
│   ├── requirements.txt       # Dependencies
│   └── .env.example           # Configurations template
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AgentWorkflowVisualizer.jsx # Multi-agent process pipeline
│   │   │   ├── ChatAssistant.jsx           # Conversational Voice & Text console
│   │   │   ├── InteractiveMap.jsx          # Leaflet routing map
│   │   │   ├── LiveStatus.jsx              # Severity warnings marquee
│   │   │   ├── NotificationPanel.jsx       # SMS logs & Contacts editor
│   │   │   └── ShelterHospitalCards.jsx    # Open camps & clinic directory
│   │   ├── App.jsx            # State manager
│   │   ├── index.css          # Design system & dark command center styles
│   │   └── main.jsx           # React app mount
│   ├── index.html             # Preloads Leaflet JS & fonts CDN
│   ├── package.json           # Node requirements
│   └── vite.config.js         # Proxy router settings to port 8000
├── diagrams/
│   ├── architecture.md        # AI components mapping & structural flowchart
│   ├── sequence.md            # Action plan chronologies
│   └── user_flow.md           # User journey branches
└── README.md
```

---

## 🚀 Setup & Launch Instructions

Sentinel AI runs out-of-the-box in **Demo Mode (Mock Mode)**, compiling mock paths, shelters, and hospital data so the app can be run without an active Gemini API key.

### Step 1: Run the FastAPI Backend
1. Navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. Create a Python virtual environment and activate it:
   ```bash
   python -m venv venv
   # On Windows (Command Prompt/Powershell):
   .\venv\Scripts\activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. (Optional) Configure your Gemini API key. Copy the env template:
   ```bash
   copy .env.example .env
   ```
   Open `.env` and enter your Google `GEMINI_API_KEY=""` to activate real AI generation.
5. Launch the backend server:
   ```bash
   python -m uvicorn app.main:app --port 8000 --reload
   ```
   *The backend will be active at `http://127.0.0.1:8000`. You can inspect the Swagger API docs at `http://127.0.0.1:8000/docs`.*

### Step 2: Run the React Frontend
1. Open a new terminal window and navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
2. Install node dependencies:
   ```bash
   npm install
   ```
3. Start the Vite dev server:
   ```bash
   npm run dev
   ```
   *The dashboard will launch on `http://localhost:3000`.*

---

## 🧠 Multi-Agent Architecture Handoff

```
[Report Query] 
   |
   v
[Decision Orchestrator] ──> Initializes State
   |
   +──> [Detection Agent] (Extracts: Disaster Category, Severity, Location, Lang)
   |
   +──> [RAG Agent] (Retrieves official NDMA protocols via Vector similarity)
   |
   +──> [Route Agent] (Plots coordinates bypassing hazard red zones)
   |
   +──> [Facility Agent] (Filters nearest shelters & active ICU hospital beds)
   |
   +──> [Notification Agent] (Formulates SMS emergency text alerts)
   |
   +──> [Translation Agent] (Translates compiled action plan to Hindi/Tamil/Telugu)
   |
   v
[Decision Orchestrator] ──> Saves Report to DB ──> Returns JSON response to UI
```

For a comprehensive explanation of our design choices and user journey paths, please consult the [System Architecture Documentation](file:///c:/Users/Jaanu/OneDrive/Desktop/hack%20ai/diagrams/architecture.md).
