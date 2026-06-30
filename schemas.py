from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ReportRequest(BaseModel):
    query: str
    language: Optional[str] = None

class ReportResponse(BaseModel):
    id: int
    query: str
    disaster_type: str
    severity: str
    location: str
    language: str
    summary: Optional[str]
    action_plan: Optional[str]
    translated_plan: Optional[str]
    timestamp: datetime

    class Config:
        orm_mode = True

class ContactCreate(BaseModel):
    name: str
    phone: str
    relationship: Optional[str] = "Family"

class ContactResponse(BaseModel):
    id: int
    name: str
    phone: str
    relationship: str

    class Config:
        orm_mode = True

class NotificationLogResponse(BaseModel):
    id: int
    contact_id: int
    message: str
    status: str
    timestamp: datetime

    class Config:
        orm_mode = True
