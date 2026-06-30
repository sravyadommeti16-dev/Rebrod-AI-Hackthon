import json
import re
import requests
from app.config import settings

class GeminiClient:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
        self.headers = {"Content-Type": "application/json"}

    def generate_text(self, prompt: str) -> str:
        if settings.is_demo_mode:
            return self._generate_mock_text(prompt)
            
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }
        try:
            response = requests.post(self.url, headers=self.headers, json=payload, timeout=30)
            if response.status_code == 200:
                data = response.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return text
            else:
                print(f"Gemini API Error {response.status_code}: {response.text}")
                return self._generate_mock_text(prompt)
        except Exception as e:
            print(f"Error calling Gemini: {e}")
            return self._generate_mock_text(prompt)

    def generate_json(self, prompt: str, fallback_mock: dict = None) -> dict:
        # Prompt the model to return JSON only
        json_prompt = prompt + "\n\nCRITICAL: Return ONLY a valid JSON object. Do not include markdown wraps, text explanation, or trailing commas."
        raw_text = self.generate_text(json_prompt).strip()
        
        # Strip markdown wraps if model ignored instructions
        if raw_text.startswith("```"):
            # Strip ```json or ``` at start
            raw_text = re.sub(r"^```(?:json)?\n", "", raw_text)
            # Strip ``` at end
            raw_text = re.sub(r"\n```$", "", raw_text)
            raw_text = raw_text.strip()
            
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: '{raw_text}'. Error: {e}")
            if settings.is_demo_mode:
                return self._generate_mock_json(prompt, fallback_mock)
            # Try to regex extract JSON block if there was surrounding text
            match = re.search(r"\{.*\}", raw_text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(0))
                except:
                    pass
            return fallback_mock or {}

    def _generate_mock_text(self, prompt: str) -> str:
        prompt_lower = prompt.lower()
        if "translate" in prompt_lower:
            if "hindi" in prompt_lower or "hi" in prompt_lower:
                return "चेतावनी: बाढ़ आ रही है। कृपया तुरंत स्कूल शिविर में सुरक्षित स्थान पर चले जाएं।"
            if "tamil" in prompt_lower or "ta" in prompt_lower:
                return "எச்சரிக்கை: வெள்ளம் சூழ்ந்துள்ளது. தயவுசெய்து உடனடியாக பள்ளி முகாமிற்குச் செல்லவும்."
            if "telugu" in prompt_lower or "te" in prompt_lower:
                return "హెచ్చరిక: వరదలు ఉన్నాయి. దయచేసి వెంటనే పాఠశాల సహాయ కేంద్రానికి వెళ్లండి."
        return "Warning: Emergency situation detected. Evacuate to the nearest relief center immediately."

    def _generate_mock_json(self, prompt: str, fallback: dict) -> dict:
        prompt_lower = prompt.lower()
        if "detect" in prompt_lower or "classify" in prompt_lower:
            # Emergency Detection Agent Mock
            disaster = "none"
            severity = "medium"
            location = "Chennai"
            is_emergency = False
            
            if "flood" in prompt_lower or "water" in prompt_lower or "submerged" in prompt_lower or "rain" in prompt_lower:
                disaster = "flood"
                severity = "critical" if "trapped" in prompt_lower or "stuck" in prompt_lower else "high"
                is_emergency = True
            elif "cyclone" in prompt_lower or "wind" in prompt_lower or "storm" in prompt_lower:
                disaster = "cyclone"
                severity = "high"
                is_emergency = True
            elif "earthquake" in prompt_lower or "quake" in prompt_lower or "shake" in prompt_lower:
                disaster = "earthquake"
                severity = "critical"
                is_emergency = True
            elif "fire" in prompt_lower or "smoke" in prompt_lower or "burning" in prompt_lower:
                disaster = "fire"
                severity = "high"
                is_emergency = True
            elif "landslide" in prompt_lower or "mud" in prompt_lower:
                disaster = "landslide"
                severity = "medium"
                is_emergency = True
                
            # Try to extract location
            loc_match = re.search(r"in\s+([a-zA-Z\s]+)", prompt)
            if loc_match:
                location = loc_match.group(1).split(",")[0].strip()

            return {
                "disaster_type": disaster,
                "severity": severity,
                "location": location,
                "is_emergency": is_emergency,
                "language": "hi" if "hindi" in prompt_lower or "हिंदी" in prompt_lower else ("ta" if "tamil" in prompt_lower or "தமிழ்" in prompt_lower else "en")
            }
        return fallback or {}

gemini_client = GeminiClient()
