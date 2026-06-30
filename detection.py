from app.utils.gemini_client import gemini_client

class DetectionAgent:
    def __init__(self):
        self.client = gemini_client

    def run(self, state: dict) -> dict:
        query = state.get("user_query", "")
        
        prompt = f"""
        Analyze the following emergency report or query.
        Extract the following parameters as a JSON object:
        1. disaster_type: One of 'flood', 'cyclone', 'earthquake', 'fire', 'landslide', or 'none'.
        2. severity: One of 'low', 'medium', 'high', 'critical'.
        3. location: The city/region mentioned, or 'Unknown'.
        4. is_emergency: Boolean indicating if this is an active life-safety emergency.
        5. language: Standard ISO code for the user's input language (e.g. 'en', 'hi', 'ta', 'te', 'bn', 'kn', 'ml').

        Report text:
        "{query}"

        Return ONLY a JSON object in this format:
        {{
            "disaster_type": "flood",
            "severity": "high",
            "location": "Chennai",
            "is_emergency": true,
            "language": "en"
        }}
        """
        
        fallback = {
            "disaster_type": "none",
            "severity": "medium",
            "location": "Unknown",
            "is_emergency": False,
            "language": "en"
        }
        
        result = self.client.generate_json(prompt, fallback_mock=fallback)
        
        # Merge results into state
        state["disaster_type"] = result.get("disaster_type", "none").lower()
        state["severity"] = result.get("severity", "medium").lower()
        state["location"] = result.get("location", "Unknown")
        state["is_emergency"] = result.get("is_emergency", False)
        
        # Maintain default language fallback
        lang = result.get("language", "en").lower()
        state["language"] = lang if lang in ["en", "hi", "ta", "te", "bn", "kn", "ml"] else "en"
        
        step_log = f"[Detection Agent]: Classified disaster as '{state['disaster_type'].upper()}' with severity '{state['severity'].upper()}' at location '{state['location']}' (Language: '{state['language']}')."
        state["execution_steps"].append(step_log)
        
        return state

detection_agent = DetectionAgent()
