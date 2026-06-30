from app.agents.detection import detection_agent
from app.agents.rag import rag_agent
from app.agents.route import route_agent
from app.agents.shelter import shelter_agent
from app.agents.hospital import hospital_agent
from app.agents.resource import resource_agent
from app.agents.notification import notification_agent
from app.agents.translation import translation_agent
from app.utils.gemini_client import gemini_client

class DecisionOrchestrator:
    def __init__(self):
        self.client = gemini_client

    def execute(self, user_query: str, target_language: str = None) -> dict:
        # Initialize the global agent state
        state = {
            "user_query": user_query,
            "language": target_language or "en",
            "disaster_type": "none",
            "severity": "medium",
            "location": "Unknown",
            "is_emergency": False,
            "rag_context": "",
            "routes": [],
            "blocked_zones": [],
            "map_center": [20.5937, 78.9629],
            "shelters": [],
            "hospitals": [],
            "resources": [],
            "emergency_sms": "",
            "notifications_sent": False,
            "final_response": "",
            "translated_plan": "",
            "execution_steps": []
        }
        
        state["execution_steps"].append("[Orchestrator]: Emergency response pipeline initiated.")
        
        # 1. Detection Agent
        state = detection_agent.run(state)
        
        # Override target language if user requested it specifically or if detected
        if target_language:
            state["language"] = target_language
            
        # 2. Information Retrieval (RAG) Agent
        state = rag_agent.run(state)
        
        # 3. Route Planning Agent
        state = route_agent.run(state)
        
        # 4. Shelter Agent
        state = shelter_agent.run(state)
        
        # 5. Hospital Agent
        state = hospital_agent.run(state)
        
        # 6. Resource Agent
        state = resource_agent.run(state)
        
        # 7. Notification Agent
        state = notification_agent.run(state)
        
        # 8. Orchestrate Final Response (English)
        state = self._generate_final_response(state)
        
        # 9. Translation Agent
        state = translation_agent.run(state)
        
        state["execution_steps"].append("[Orchestrator]: Pipeline complete. Dispatching results to Emergency Command Center.")
        return state

    def _generate_final_response(self, state: dict) -> dict:
        disaster = state["disaster_type"].upper()
        severity = state["severity"].upper()
        location = state["location"]
        rag_context = state["rag_context"]
        routes = state["routes"]
        shelters = state["shelters"]
        hospitals = state["hospitals"]
        
        primary_route = routes[0] if routes else None
        primary_shelter = shelters[0] if shelters else None
        primary_hospital = hospitals[0] if hospitals else None
        
        # Formulate instructions for LLM to compile details
        prompt = f"""
        You are the Decision Orchestrator Agent for Sentinel AI Disaster Response.
        Compile a clear, concise, and highly actionable Emergency Evacuation Plan based on the data below.
        
        Disaster: {disaster} (Severity: {severity})
        Location: {location}
        
        NDMA Safety Guidelines:
        {rag_context}
        
        Recommended Evacuation Route:
        - Name: {primary_route['name'] if primary_route else 'N/A'}
        - Distance/Duration: {primary_route['distance'] if primary_route else 'N/A'} / {primary_route['duration'] if primary_route else 'N/A'}
        - Condition: {primary_route['condition'] if primary_route else 'N/A'}
        
        Recommended Shelter:
        - Name: {primary_shelter['name'] if primary_shelter else 'N/A'}
        - Occupancy: {primary_shelter['occupancy'] if primary_shelter else 'N/A'}
        - Phone: {primary_shelter['phone'] if primary_shelter else 'N/A'}
        
        Recommended Hospital:
        - Name: {primary_hospital['name'] if primary_hospital else 'N/A'}
        - Bed Capacity: {primary_hospital['icu_beds'] if primary_hospital else 'N/A'}
        - Phone: {primary_hospital['phone'] if primary_hospital else 'N/A'}
        
        Format the plan under these markdown sections:
        ### 🚨 EMERGENCY STATUS: [Disaster Type] in [Location] ([Severity] Risk)
        ### 🏃 IMMEDIATE ACTION PLAN
        (Bullet points of exactly what to do step-by-step)
        ### 🛣️ EVACUATION & MEDICAL DETAILS
        (Summarize recommended route, shelter, and hospital beds)
        """
        
        # Compile fallback summary in case of demo mode or generation error
        fallback_plan = (
            f"### 🚨 EMERGENCY STATUS: {disaster} in {location} ({severity} Risk)\n\n"
            f"### 🏃 IMMEDIATE ACTION PLAN\n"
            f"* **Evacuate immediately**: Seek higher ground or follow structural safety procedures.\n"
            f"* **Follow Safety Guidelines**: {rag_context.split('Guidelines: ')[-1] if 'Guidelines: ' in rag_context else 'Move to safe areas, avoid flood waters.'}\n"
            f"* **Notifications Queued**: Emergency contacts and disaster control room have been drafted with SMS updates.\n\n"
            f"### 🛣️ EVACUATION & MEDICAL DETAILS\n"
            f"* **Route**: Use **{primary_route['name'] if primary_route else 'Safe Road'}** ({primary_route['distance'] if primary_route else 'N/A'} - {primary_route['duration'] if primary_route else 'N/A'}). Condition: {primary_route['condition'] if primary_route else 'N/A'}.\n"
            f"* **Shelter**: Head to **{primary_shelter['name'] if primary_shelter else 'Nearest Safe Shelter'}** (Occupancy: {primary_shelter['occupancy'] if primary_shelter else 'N/A'}). Call: {primary_shelter['phone'] if primary_shelter else 'N/A'}.\n"
            f"* **Medical**: Nearest active clinic is **{primary_hospital['name'] if primary_hospital else 'Emergency Center'}** (ICU Beds: {primary_hospital['icu_beds'] if primary_hospital else 'N/A'}). Call: {primary_hospital['phone'] if primary_hospital else 'N/A'}."
        )
        
        plan = self.client.generate_text(prompt)
        if not self.client.api_key or len(plan) < 100:
            plan = fallback_plan
            
        state["final_response"] = plan
        
        log_msg = f"[Orchestrator Agent]: Consolidated multi-agent outcomes into final emergency evacuation plan."
        state["execution_steps"].append(log_msg)
        return state

orchestrator_agent = DecisionOrchestrator()
