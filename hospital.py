class HospitalAgent:
    def run(self, state: dict) -> dict:
        location = state.get("location", "Unknown").lower()
        disaster_type = state.get("disaster_type", "none")
        
        # Seed mock hospitals based on location
        hospitals = []
        if "chennai" in location or disaster_type == "flood":
            hospitals = [
                {
                    "name": "Apollo Emergency Clinic",
                    "location": "Greams Road, Chennai",
                    "latlng": [13.0600, 80.2500],
                    "distance": "2.1 km",
                    "icu_beds": "12 available",
                    "oxygen_status": "Sufficient",
                    "phone": "+91 44 2829 0200",
                    "status": "Trauma Center Active (Accessible)"
                },
                {
                    "name": "Government General Hospital",
                    "location": "Park Town, Chennai",
                    "latlng": [13.0810, 80.2780],
                    "distance": "0.9 km",
                    "icu_beds": "4 available (High inflow)",
                    "oxygen_status": "Sufficient",
                    "phone": "+91 44 2530 5000",
                    "status": "Active (High Traffic - flood bypass route recommended)"
                }
            ]
        elif "mumbai" in location or disaster_type == "cyclone":
            hospitals = [
                {
                    "name": "KEM Emergency Hospital",
                    "location": "Parel, Mumbai",
                    "latlng": [19.0020, 72.8420],
                    "distance": "4.2 km",
                    "icu_beds": "8 available",
                    "oxygen_status": "Sufficient",
                    "phone": "+91 22 2410 7000",
                    "status": "Active (Trauma Ward Open)"
                }
            ]
        elif "uttarakhand" in location or disaster_type == "landslide":
            hospitals = [
                {
                    "name": "Max Super Speciality Hospital",
                    "location": "Malsi, Dehradun",
                    "latlng": [30.3800, 78.0750],
                    "distance": "6.5 km",
                    "icu_beds": "15 available",
                    "oxygen_status": "Sufficient",
                    "phone": "+91 135 719 3000",
                    "status": "Active (Road open, ambulance services running)"
                }
            ]
        else:
            # Fallback
            hospitals = [
                {
                    "name": "District General Hospital",
                    "location": "Town Center Ward 1",
                    "latlng": [20.5900, 78.9600],
                    "distance": "1.2 km",
                    "icu_beds": "5 available",
                    "oxygen_status": "Sufficient",
                    "phone": "+91 99999 22222",
                    "status": "Active (Normal Operations)"
                }
            ]
            
        state["hospitals"] = hospitals
        log_msg = f"[Hospital Agent]: Identified {len(hospitals)} operational hospitals with open emergency ICU beds."
        state["execution_steps"].append(log_msg)
        return state

hospital_agent = HospitalAgent()
