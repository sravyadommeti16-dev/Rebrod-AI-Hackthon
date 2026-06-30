class ResourceCoordinationAgent:
    def run(self, state: dict) -> dict:
        location = state.get("location", "Unknown").lower()
        disaster_type = state.get("disaster_type", "none")
        
        # Seed mock resources based on location
        resources = []
        if "chennai" in location or disaster_type == "flood":
            resources = [
                {
                    "hub_name": "Central Railway Station Depot",
                    "latlng": [13.0827, 80.2707],
                    "food_packets": "1200 units",
                    "water_liters": "3000 L",
                    "first_aid_kits": "150 kits",
                    "dry_clothes": "400 sets",
                    "status": "High Stock"
                },
                {
                    "hub_name": "Egmore Relief Depot",
                    "latlng": [13.0720, 80.2580],
                    "food_packets": "400 units",
                    "water_liters": "1000 L",
                    "first_aid_kits": "50 kits",
                    "dry_clothes": "100 sets",
                    "status": "Medium Stock (Replenishing)"
                }
            ]
        elif "mumbai" in location or disaster_type == "cyclone":
            resources = [
                {
                    "hub_name": "Bandra Stadium Relief Depot",
                    "latlng": [19.0520, 72.8250],
                    "food_packets": "2000 units",
                    "water_liters": "5000 L",
                    "first_aid_kits": "300 kits",
                    "dry_clothes": "1000 sets",
                    "status": "High Stock"
                }
            ]
        elif "uttarakhand" in location or disaster_type == "landslide":
            resources = [
                {
                    "hub_name": "Dehradun Supply Airbase",
                    "latlng": [30.1900, 78.1800],
                    "food_packets": "5000 units (Airdrop Ready)",
                    "water_liters": "10000 L",
                    "first_aid_kits": "500 kits",
                    "dry_clothes": "1200 sets",
                    "status": "Airdrop Depot Operational"
                }
            ]
        else:
            resources = [
                {
                    "hub_name": "Local Panchayat Supply Office",
                    "latlng": [20.5937, 78.9629],
                    "food_packets": "300 units",
                    "water_liters": "800 L",
                    "first_aid_kits": "30 kits",
                    "dry_clothes": "50 sets",
                    "status": "Stock Available"
                }
            ]
            
        state["resources"] = resources
        log_msg = f"[Resource Agent]: Allocated {len(resources)} local emergency hubs containing food, water, and first aid packages."
        state["execution_steps"].append(log_msg)
        return state

resource_agent = ResourceCoordinationAgent()
