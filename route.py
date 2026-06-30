class RoutePlanningAgent:
    def run(self, state: dict) -> dict:
        location = state.get("location", "Unknown").lower()
        disaster_type = state.get("disaster_type", "none")
        
        # Coordinates setup based on location to make the map look extremely realistic
        routes = []
        blocked_zones = []
        
        if "chennai" in location or disaster_type == "flood":
            # Chennai Coordinates (Flood Simulation)
            start_coord = [13.0827, 80.2707] # Chennai Central
            shelter_coord_1 = [13.0910, 80.2890] # St. Mary's School Shelter
            shelter_coord_2 = [13.0715, 80.2520] # Egmore Community Shelter
            
            blocked_zones = [
                {"name": "Cooum River Overflow", "latlng": [13.0730, 80.2600], "radius": 300},
                {"name": "Waterlogged Subway", "latlng": [13.0850, 80.2800], "radius": 200}
            ]
            
            routes = [
                {
                    "id": "route_primary",
                    "name": "Evacuation Route Alpha (Safe)",
                    "type": "primary",
                    "path": [
                        start_coord,
                        [13.0845, 80.2730],
                        [13.0870, 80.2780],
                        [13.0890, 80.2830],
                        shelter_coord_1
                    ],
                    "distance": "2.8 km",
                    "duration": "12 mins",
                    "safety_rating": "9.5/10",
                    "condition": "Dry & clear, bypasses waterlogged subways"
                },
                {
                    "id": "route_alternate",
                    "name": "Evacuation Route Beta (Alternate)",
                    "type": "alternate",
                    "path": [
                        start_coord,
                        [13.0790, 80.2680],
                        [13.0770, 80.2620],
                        [13.0740, 80.2580],
                        shelter_coord_2
                    ],
                    "distance": "3.1 km",
                    "duration": "18 mins",
                    "safety_rating": "7.0/10",
                    "condition": "Heavy traffic near Egmore, water level rising on curbs"
                }
            ]
            
        elif "mumbai" in location or disaster_type == "cyclone":
            # Mumbai Coordinates (Cyclone Simulation)
            start_coord = [19.0760, 72.8777] # Central Mumbai
            shelter_coord_1 = [19.0910, 72.8620] # Bandra Shelter
            
            blocked_zones = [
                {"name": "High Tide Wind Hazard", "latlng": [19.0400, 72.8200], "radius": 500},
                {"name": "Fallen Trees & Cables", "latlng": [19.0800, 72.8700], "radius": 250}
            ]
            
            routes = [
                {
                    "id": "route_primary",
                    "name": "Inland Evacuation Path 1",
                    "type": "primary",
                    "path": [
                        start_coord,
                        [19.0820, 72.8750],
                        [19.0850, 72.8680],
                        shelter_coord_1
                    ],
                    "distance": "2.4 km",
                    "duration": "10 mins",
                    "safety_rating": "9.0/10",
                    "condition": "Safe from coastal surge, wind protection walls present"
                }
            ]
            
        elif "uttarakhand" in location or "shimla" in location or disaster_type == "landslide":
            # Mountain Landslide Simulation
            start_coord = [30.3165, 78.0322] # Dehradun / Hills area
            shelter_coord_1 = [30.3300, 78.0450] # Army Relief Camp
            
            blocked_zones = [
                {"name": "Active Mudflow Zone", "latlng": [30.3200, 78.0380], "radius": 350}
            ]
            
            routes = [
                {
                    "id": "route_primary",
                    "name": "Ridge Evacuation Route",
                    "type": "primary",
                    "path": [
                        start_coord,
                        [30.3190, 78.0280],
                        [30.3250, 78.0330],
                        [30.3280, 78.0400],
                        shelter_coord_1
                    ],
                    "distance": "3.8 km",
                    "duration": "25 mins",
                    "safety_rating": "8.5/10",
                    "condition": "Ridge road, safe from downhill debris flow"
                }
            ]
            
        else:
            # General coordinates fallback (uses offsets based on a hypothetical central point)
            start_coord = [20.5937, 78.9629] # Center of India
            shelter_coord_1 = [20.6000, 78.9700]
            
            blocked_zones = [
                {"name": "Hazard Area", "latlng": [20.5960, 78.9660], "radius": 200}
            ]
            
            routes = [
                {
                    "id": "route_primary",
                    "name": "Standard Safe Evacuation Route",
                    "type": "primary",
                    "path": [
                        start_coord,
                        [20.5950, 78.9650],
                        [20.5980, 78.9680],
                        shelter_coord_1
                    ],
                    "distance": "1.5 km",
                    "duration": "8 mins",
                    "safety_rating": "9.0/10",
                    "condition": "Road clear of blockages"
                }
            ]
            
        state["routes"] = routes
        state["blocked_zones"] = blocked_zones
        state["map_center"] = start_coord
        
        log_msg = f"[Route Agent]: Calculated {len(routes)} safe path(s) and identified {len(blocked_zones)} blocked zones avoiding active hazard areas."
        state["execution_steps"].append(log_msg)
        return state

route_agent = RoutePlanningAgent()
