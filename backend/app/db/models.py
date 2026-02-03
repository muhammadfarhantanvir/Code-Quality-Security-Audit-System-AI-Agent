from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .session import Base

class Scan(Base):
    __tablename__ = "scans"

    id = Column(String, primary_key=True, index=True)
    github_url = Column(String)
    status = Column(String) # pending, processing, completed, failed
    risk_score = Column(Float, default=0.0)
    total_issues = Column(Integer, default=0)
    files_scanned = Column(Integer, default=0)
    total_lines = Column(Integer, default=0)
    duration = Column(Float, default=0.0)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    issues = relationship("Issue", back_populates="scan", cascade="all, delete-orphan")

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(String, ForeignKey("scans.id"))
    issue_id = Column(String) # For pattern ID
    name = Column(String)
    description = Column(Text)
    severity = Column(String)
    category = Column(String)
    file_path = Column(String)
    line_number = Column(Integer)
    code_snippet = Column(Text)
    recommendation = Column(Text)
    ai_insight = Column(Text, nullable=True)
    compliance_tags = Column(String, nullable=True) # JSON string of tags
    
    scan = relationship("Scan", back_populates="issues")
