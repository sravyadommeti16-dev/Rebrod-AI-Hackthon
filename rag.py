from app.utils.rag_store import rag_store

class RAGAgent:
    def run(self, state: dict) -> dict:
        disaster_type = state.get("disaster_type", "none")
        query = state.get("user_query", "")
        
        # Query local vector store
        # We can combine the user query and disaster type for richer retrieval
        search_query = f"{disaster_type} {query}"
        results = rag_store.retrieve(search_query, limit=2)
        
        if results:
            context_blocks = []
            for doc in results:
                context_blocks.append(f"Source: {doc['title']}\nGuidelines: {doc['content']}")
            state["rag_context"] = "\n\n".join(context_blocks)
            log_msg = f"[RAG Agent]: Retrieved official guidelines for category '{disaster_type.upper()}' (Match Score: {results[0]['score']:.2f})."
        else:
            state["rag_context"] = "No official NDMA guidelines found for this request. Please exercise general emergency safety caution."
            log_msg = "[RAG Agent]: No specific safety guidelines found. Loaded general caution protocols."
            
        state["execution_steps"].append(log_msg)
        return state

rag_agent = RAGAgent()
