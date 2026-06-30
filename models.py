import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship as orm_relationship
from app.database import Base

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text, nullable=False)
    disaster_type = Column(String(50), default="none")
    severity = Column(String(50), default="medium")
    location = Column(String(100), default="Unknown")
    language = Column(String(10), default="en")
    summary = Column(Text, nullable=True)
    action_plan = Column(Text, nullable=True)
    translated_plan = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    relationship = Column(String(50), default="Family")
    
    notifications = orm_relationship("NotificationLog", back_populates="contact", cascade="all, delete-orphan")

class NotificationLog(Base):
    __tablename__ = "notification_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(50), default="Sent")
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    contact = orm_relationship("Contact", back_populates="notifications")
