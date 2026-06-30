class NotificationAgent:
    def run(self, state: dict) -> dict:
        disaster_type = state.get("disaster_type", "none").upper()
        severity = state.get("severity", "MEDIUM").upper()
        location = state.get("location", "Unknown")
        shelters = state.get("shelters", [])
        
        shelter_name = shelters[0]["name"] if shelters else "Nearest Safe Shelter"
        shelter_phone = shelters[0]["phone"] if shelters else "108"
        
        # Formulate emergency SMS message
        sms_text = (
            f"⚠️ SENTINEL AI EMERGENCY ALERT ⚠️\n"
            f"Disaster: {disaster_type} ({severity})\n"
            f"Location: {location}\n"
            f"Action: Evacuate immediately to {shelter_name}.\n"
            f"Contact: {shelter_phone}\n"
            f"Evacuation Map link: http://sentinel-ai.emergency/map-route"
        )
        
        state["emergency_sms"] = sms_text
        state["notifications_sent"] = True
        
        log_msg = f"[Notification Agent]: Prepared broadcast alert dispatch and contact SMS drafts: '{disaster_type} Alert at {location}'."
        state["execution_steps"].append(log_msg)
        return state

notification_agent = NotificationAgent()
