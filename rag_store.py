from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Seed NDMA protocols and guidelines
EMERGENCY_PROTOCOLS = [
    {
        "id": "flood_before",
        "category": "flood",
        "title": "Pre-Flood Preparedness Guidelines",
        "content": "Before a flood: Prepare an emergency kit (food, water, medicine, flashlight, radio). Store vital documents in waterproof bags. Identify local elevated safe zones and evacuation routes. Keep emergency contacts handy."
    },
    {
        "id": "flood_during",
        "category": "flood",
        "title": "Safety Protocols During Flooding",
        "content": "During a flood: Move to higher ground immediately. Do NOT walk, swim, or drive through moving water - just 6 inches of moving water can knock you down. Disconnect utilities and main electricity lines to prevent electrocution."
    },
    {
        "id": "flood_after",
        "category": "flood",
        "title": "Post-Flood Safety Guidelines",
        "content": "After a flood: Return home only when officials declare it safe. Avoid standing water as it may be contaminated or electrically charged. Boil all drinking water. Watch out for snakes or other animals that may have entered your home."
    },
    {
        "id": "cyclone_before",
        "category": "cyclone",
        "title": "Pre-Cyclone Warning Protocol",
        "content": "Before a cyclone: Board up windows and secure loose outdoor objects. Trim tree branches close to your house. Store food, drinking water, and essential medicines. Monitor weather bulletins on radio or TV."
    },
    {
        "id": "cyclone_during",
        "category": "cyclone",
        "title": "Survival Guidelines During Cyclone Landfall",
        "content": "During a cyclone: Stay indoors, preferably in the center of the house or an inner windowless room. Disconnect main power lines. If the wind goes calm, do not go outside, as the 'eye' of the storm is passing and winds will resume shortly."
    },
    {
        "id": "cyclone_after",
        "category": "cyclone",
        "title": "Post-Cyclone Recovery",
        "content": "After a cyclone: Do not go near fallen power poles or loose wires. Report broken lines to authorities. Clean up debris safely, wear protective boots and gloves. Avoid eating damp or exposed food."
    },
    {
        "id": "earthquake_during_in",
        "category": "earthquake",
        "title": "Earthquake Safety Protocols - Indoors",
        "content": "During an earthquake (Indoors): Drop, Cover, and Hold On. Drop to your knees, take cover under a sturdy desk or table, and hold onto it. Stay away from glass windows, mirrors, cabinets, and exterior walls."
    },
    {
        "id": "earthquake_during_out",
        "category": "earthquake",
        "title": "Earthquake Safety Protocols - Outdoors",
        "content": "During an earthquake (Outdoors): Move to an open area away from buildings, trees, power lines, and streetlights. If driving, pull over to a safe area away from overpasses, bridges, and power lines, and remain in the vehicle."
    },
    {
        "id": "earthquake_after",
        "category": "earthquake",
        "title": "Post-Earthquake Safety & Checklist",
        "content": "After an earthquake: Expect aftershocks. Check yourself and others for injuries. Do NOT use elevators; take the stairs. Inspect utilities for gas leaks, water damage, or electrical shorts. Fire is the most common hazard after a quake."
    },
    {
        "id": "fire_action",
        "category": "fire",
        "title": "Immediate Action in Fire Emergencies",
        "content": "In case of fire: Alert others immediately. Crawl low under smoke to exit the building - the cleanest air is near the floor. Feel doors with the back of your hand before opening; if hot, find another exit. Do NOT use elevators. Call fire services (101)."
    },
    {
        "id": "fire_first_aid",
        "category": "fire",
        "title": "Fire First Aid & Survival Techniques",
        "content": "If your clothes catch fire: Stop, Drop, and Roll. Cover your face with your hands and roll back and forth to extinguish flames. Cool minor burns with cool running water for 10-15 minutes. Call for medical assistance."
    },
    {
        "id": "landslide_during",
        "category": "landslide",
        "title": "Landslide & Mudflow Evacuation Plan",
        "content": "During a landslide: Evacuate immediately if safety allows. Stay alert for unusual sounds like cracking trees or knocking rocks, which indicate shifting earth. Avoid river channels and low-lying valleys. If trapped, roll into a tight ball to protect your head."
    }
]

class RAGStore:
    def __init__(self):
        self.documents = EMERGENCY_PROTOCOLS
        self.texts = [doc["content"] for doc in self.documents]
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.texts)

    def retrieve(self, query: str, limit: int = 2) -> list:
        if not query:
            return []
        
        # Vectorize query and calculate cosine similarity
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Sort documents by similarity score
        top_indices = np.argsort(similarities)[::-1]
        
        results = []
        for idx in top_indices[:limit]:
            if similarities[idx] > 0.05:  # Relevance threshold
                doc = self.documents[idx].copy()
                doc["score"] = float(similarities[idx])
                results.append(doc)
                
        # If no semantic matches, return default general instructions based on basic categories
        if not results:
            query_lower = query.lower()
            for cat in ["flood", "cyclone", "earthquake", "fire", "landslide"]:
                if cat in query_lower:
                    for doc in self.documents:
                        if doc["category"] == cat:
                            doc_copy = doc.copy()
                            doc_copy["score"] = 0.1
                            results.append(doc_copy)
                    break
                    
        return results[:limit]

rag_store = RAGStore()
