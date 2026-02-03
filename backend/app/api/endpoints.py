from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import tempfile
import shutil
import subprocess
import json
from datetime import datetime

from ..core.auditor import CodeAuditor
from ..services.ollama_service import OllamaService
from ..db.session import get_db, SessionLocal, engine
from ..db import models

# Create tables
models.Base.metadata.create_all(bind=engine)

router = APIRouter()
auditor = CodeAuditor()
ollama = OllamaService()

class ScanRequest(BaseModel):
    github_url: str
    use_ai: bool = False

class ScanResponse(BaseModel):
    id: str
    status: str
    message: str

@router.post("/scan", response_model=ScanResponse)
async def start_scan(request: ScanRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    scan_id = os.urandom(8).hex()
    
    # Create scan record
    db_scan = models.Scan(
        id=scan_id,
        github_url=request.github_url,
        status="processing"
    )
    db.add(db_scan)
    db.commit()
    
    background_tasks.add_task(perform_github_scan, scan_id, request.github_url, request.use_ai)
    
    return ScanResponse(
        id=scan_id,
        status="accepted",
        message="Scan started in background"
    )

@router.get("/scans", response_model=List[Dict[str, Any]])
async def list_scans(db: Session = Depends(get_db)):
    scans = db.query(models.Scan).order_by(models.Scan.created_at.desc()).limit(10).all()
    return [{"id": s.id, "url": s.github_url, "score": s.risk_score, "date": s.created_at, "issues": s.total_issues} for s in scans]

@router.get("/scan/{scan_id}")
async def get_scan_result(scan_id: str, db: Session = Depends(get_db)):
    scan = db.query(models.Scan).filter(models.Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
        
    if scan.status == "failed":
        return {
            "id": scan.id,
            "status": "failed",
            "error": scan.error_message or "Unknown audit error",
            "url": scan.github_url
        }
        
    issues = db.query(models.Issue).filter(models.Issue.scan_id == scan_id).all()

    # Handle case where issues might be None
    issues_list = issues if issues is not None else []

    return {
        "id": scan.id,
        "status": scan.status,
        "url": scan.github_url,
        "created_at": scan.created_at,
        "results": {
            "summary": {
                "files_scanned": scan.files_scanned,
                "total_lines": scan.total_lines,
                "risk_score": scan.risk_score,
                "duration": scan.duration,
                "total_issues": scan.total_issues
            },
            "issues": [
                {
                    "id": i.issue_id,
                    "name": i.name,
                    "description": i.description,
                    "severity": i.severity,
                    "category": i.category,
                    "line": i.line_number,
                    "snippet": i.code_snippet,
                    "recommendation": i.recommendation,
                    "file": i.file_path,
                    "ai_insight": i.ai_insight
                } for i in issues_list
            ]
        }
    }

def perform_github_scan(scan_id: str, github_url: str, use_ai: bool):
    # Get a fresh DB session for the background thread
    db = SessionLocal()
    
    # Clean URL
    github_url = github_url.strip().rstrip('/')
    if 'github.com' in github_url:
        parts = github_url.split('/')
        if len(parts) > 5 and (parts[4] == 'tree' or parts[4] == 'blob'):
            github_url = "/".join(parts[:5])
            
    temp_dir = tempfile.mkdtemp()
    try:
        process = subprocess.run(
            ["git", "clone", "--depth", "1", github_url, temp_dir],
            check=False,
            capture_output=True,
            text=True
        )
        
        if process.returncode != 0:
            error_msg = process.stderr.strip() or f"Git clone failed with exit code {process.returncode}"
            print(f"[ERROR] Git clone failed: {error_msg}")
            
            # User-friendly error mapping
            if "not found" in error_msg.lower():
                user_msg = "Repository not found or access denied (Private Repo)."
            elif "could not resolve host" in error_msg.lower():
                user_msg = "Network error: Could not connect to GitHub."
            else:
                user_msg = error_msg

            db_scan = db.query(models.Scan).filter(models.Scan.id == scan_id).first()
            if db_scan:
                db_scan.status = "failed"
                db_scan.error_message = user_msg
                db_scan.risk_score = 0
                db.commit()
            return

        # Perform Scan
        results = auditor.scan_directory(temp_dir)

        # Check if results is valid and contains required keys
        if not results or 'summary' not in results or 'issues' not in results:
            raise Exception("Invalid scan results format returned by auditor")

        summary = results['summary']
        issues_list = results['issues'] if results['issues'] is not None else []

        # Update Scan record
        db_scan = db.query(models.Scan).filter(models.Scan.id == scan_id).first()
        if db_scan:
            db_scan.status = "completed"
            db_scan.risk_score = summary['risk_score']
            db_scan.total_issues = summary['total_issues']
            db_scan.files_scanned = summary['files_scanned']
            db_scan.total_lines = summary['total_lines']
            db_scan.duration = summary['duration']

            # Save issues
            for idx, issue_data in enumerate(issues_list):
                ai_insight = None
                if use_ai and idx < 5:  # Use index instead of searching for the item
                    ai_insight = ollama.analyze_code(issue_data['snippet'], issue_data['name'])

                db_issue = models.Issue(
                    scan_id=scan_id,
                    issue_id=issue_data['id'],
                    name=issue_data['name'],
                    description=issue_data['description'],
                    severity=issue_data['severity'],
                    category=issue_data['category'],
                    file_path=issue_data['file'],
                    line_number=issue_data['line'],
                    code_snippet=issue_data['snippet'],
                    recommendation=issue_data['recommendation'],
                    ai_insight=ai_insight,
                    compliance_tags=json.dumps(issue_data.get('compliance', []))
                )
                db.add(db_issue)

            db.commit()
            
    except Exception as e:
        print(f"[CRITICAL] Scan task failed: {e}")
        import traceback
        print(f"[CRITICAL] Full traceback: {traceback.format_exc()}")
        db_scan = db.query(models.Scan).filter(models.Scan.id == scan_id).first()
        if db_scan:
            db_scan.status = "failed"
            db_scan.error_message = f"Internal Exception: {str(e)}"
            db.commit()
    finally:
        db.close()
        shutil.rmtree(temp_dir)
