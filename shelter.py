class ShelterAgent:
    def run(self, state: dict) -> dict:
        location = state.get("location", "Unknown").lower()
        disaster_type = state.get("disaster_type", "none")
        
        # Seed mock shelters based on location
        shelters = []
        if "chennai" in location or disaster_type == "flood":
            shelters = [
                {
                    "name": "St. Mary's School Relief Camp",
                    "location": "George Town, Chennai",
                    "latlng": [13.0910, 80.2890],
                    "distance": "2.8 km",
                    "occupancy": "142/350",
                    "status": "Active (Open)",
                    "supplies": ["Food & Water", "Medical Support", "Dry Clothing"],
                    "phone": "+91 44 2524 1001"
                },
                {
                    "name": "Egmore Community Hall Shelter",
                    "location": "Egmore, Chennai",
                    "latlng": [13.0715, 80.2520],
                    "distance": "3.1 km",
                    "occupancy": "285/300",
                    "status": "Active (Near Capacity)",
                    "supplies": ["Drinking Water", "First Aid Kit", "Rest Beds"],
                    "phone": "+91 44 2819 2002"
                }
            ]
        elif "mumbai" in location or disaster_type == "cyclone":
            shelters = [
                {
                    "name": "Bandra West Municipal School Shelter",
                    "location": "Bandra, Mumbai",
                    "latlng": [19.0910, 72.8620],
                    "distance": "2.4 km",
                    "occupancy": "95/200",
                    "status": "Active (Open)",
                    "supplies": ["Prepared Meals", "Doctor On-Call", "Blankets"],
                    "phone": "+91 22 2640 3003"
                }
            ]
        elif "uttarakhand" in location or disaster_type == "landslide":
            shelters = [
                {
                    "name": "Army Base Campsite",
                    "location": "Rajpur Road, Dehradun",
                    "latlng": [30.3300, 78.0450],
                    "distance": "3.8 km",
                    "occupancy": "180/500",
                    "status": "Active (Open)",
                    "supplies": ["Satellite Phones", "Helipad Access", "Emergency Rations"],
                    "phone": "+91 135 274 4004"
                }
            ]
        else:
            # Fallback
            shelters = [
                {
                    "name": "Central Community Relief Center",
                    "location": "District HQ Center",
                    "latlng": [20.6000, 78.9700],
                    "distance": "1.5 km",
                    "occupancy": "50/200",
                    "status": "Active (Open)",
                    "supplies": ["Water", "Rations", "Basic First Aid"],
                    "phone": "+91 99999 11111"
                }
            ]
            
        state["shelters"] = shelters
        log_msg = f"[Shelter Agent]: Recommended {len(shelters)} active relief shelter camps in the vicinity."
        state["execution_steps"].append(log_msg)
        return state

shelter_agent = ShelterAgent()
