import logging
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from app.config import settings
from app.database import engine, get_db, Base
from app.models.models import Report, Contact, NotificationLog
from app.models.schemas import ReportRequest, ContactCreate, ContactResponse, NotificationLogResponse
from app.agents.orchestrator import orchestrator_agent

# Initialize Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sentinel-ai")

# Initialize Database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Emergency Multi-Agent Disaster Response Copilot Backend Services",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Seed database with default emergency contacts if table is empty
@app.on_event("startup")
def seed_contacts():
    db = next(get_db())
    try:
        if db.query(Contact).count() == 0:
            defaults = [
                Contact(name="Disaster Management Control Room", phone="+91 11 2436 3260", relationship="Authority Office"),
                Contact(name="Primary Emergency Responder (108)", phone="108", relationship="Ambulance Services"),
                Contact(name="Disaster Helpline", phone="1078", relationship="NDRF Helpline"),
                Contact(name="Local Fire Services (101)", phone="101", relationship="Fire Station"),
            ]
            db.add_all(defaults)
            db.commit()
            logger.info("Successfully seeded default emergency contacts.")
    except Exception as e:
        logger.error(f"Error during contact seeding: {e}")
    finally:
        db.close()

@app.get("/")
def read_root():
    return {
        "status": "online",
        "project": settings.PROJECT_NAME,
        "demo_mode": settings.is_demo_mode
    }

@app.post("/api/disaster/report")
def report_disaster(req: ReportRequest, db: Session = Depends(get_db)):
    logger.info(f"Received emergency query: '{req.query}'")
    try:
        # Run the Multi-Agent orchestrator pipeline
        agent_outcome = orchestrator_agent.execute(req.query, req.language)
        
        # Save report to Database
        db_report = Report(
            query=agent_outcome["user_query"],
            disaster_type=agent_outcome["disaster_type"],
            severity=agent_outcome["severity"],
            location=agent_outcome["location"],
            language=agent_outcome["language"],
            summary=agent_outcome["rag_context"][:200] + "...", # Short summary from RAG
            action_plan=agent_outcome["final_response"],
            translated_plan=agent_outcome["translated_plan"]
        )
        db.add(db_report)
        db.commit()
        db.refresh(db_report)
        
        # Simulating Emergency Notification broadcasts for all configured contacts
        contacts = db.query(Contact).all()
        notification_logs = []
        is_sent = agent_outcome.get("notifications_sent", False)
        for contact in contacts:
            log_entry = NotificationLog(
                contact_id=contact.id,
                message=agent_outcome["emergency_sms"],
                status="Sent" if is_sent else "Failed"
            )
            db.add(log_entry)
            notification_logs.append(log_entry)
            
        if notification_logs:
            db.commit()
            
        # Return state output formatted with DB ids
        response_data = {
            "report_id": db_report.id,
            "disaster_type": agent_outcome["disaster_type"],
            "severity": agent_outcome["severity"],
            "location": agent_outcome["location"],
            "language": agent_outcome["language"],
            "rag_context": agent_outcome["rag_context"],
            "routes": agent_outcome["routes"],
            "blocked_zones": agent_outcome["blocked_zones"],
            "map_center": agent_outcome["map_center"],
            "shelters": agent_outcome["shelters"],
            "hospitals": agent_outcome["hospitals"],
            "resources": agent_outcome["resources"],
            "emergency_sms": agent_outcome["emergency_sms"],
            "notifications_sent": agent_outcome["notifications_sent"],
            "final_response": agent_outcome["final_response"],
            "translated_plan": agent_outcome["translated_plan"],
            "execution_steps": agent_outcome["execution_steps"]
        }
        return response_data
        
    except Exception as e:
        logger.error(f"Error handling emergency report: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred in orchestrator workflow: {str(e)}"
        )

# Emergency Contacts Management API
@app.get("/api/contacts", response_model=List[ContactResponse])
def get_contacts(db: Session = Depends(get_db)):
    return db.query(Contact).all()

@app.post("/api/contacts", response_model=ContactResponse)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = Contact(name=contact.name, phone=contact.phone, relationship=contact.relationship)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@app.delete("/api/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return {"message": f"Successfully deleted contact {contact_id}"}

# Notification Logs API
@app.get("/api/notifications")
def get_notifications(db: Session = Depends(get_db)):
    logs = db.query(NotificationLog).order_by(NotificationLog.timestamp.desc()).limit(15).all()
    results = []
    for log in logs:
        results.append({
            "id": log.id,
            "contact_name": log.contact.name,
            "contact_phone": log.contact.phone,
            "message": log.message,
            "status": log.status,
            "timestamp": log.timestamp
        })
    return results

# Reports Logs API
@app.get("/api/reports")
def get_reports(db: Session = Depends(get_db)):
    return db.query(Report).order_by(Report.timestamp.desc()).limit(10).all()
