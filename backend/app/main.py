# backend/app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import uuid
import json
import os

# --- Configuration ---
ASSESSMENTS_FILE = "assessments.json"

# --- FastAPI App Initialization ---
app = FastAPI(title="Rubrix Basketball Assessment")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Models ---
class Student(BaseModel):
    id: str
    name: str
    group: str  # A, B, C, D

class Assessment(BaseModel):
    student_id: str
    criterion: str  # "dribbling", "passing", "shooting", "defense"
    grade: int     # 1-5 (1+=1, 1=2, 2=3, 3=4, 4=5)
    notes: Optional[str] = None
    timestamp: Optional[datetime] = None

# --- Database (JSON file) ---
def load_assessments():
    if not os.path.exists(ASSESSMENTS_FILE):
        return []
    with open(ASSESSMENTS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_assessments(db):
    with open(ASSESSMENTS_FILE, "w") as f:
        json.dump(db, f, indent=4, default=str)

assessments_db = load_assessments()

# --- Student Data (Hardcoded) ---
# Your 28 students in 4 groups - perfect for PE class management
STUDENTS = [
    # Group A (7 students)
    Student(id="001", name="Ahmed Al-Rashid", group="A"),
    Student(id="002", name="Sarah Johnson", group="A"),
    Student(id="003", name="Kai Chen", group="A"),
    Student(id="004", name="Fatima Hassan", group="A"),
    Student(id="005", name="Marcus Williams", group="A"),
    Student(id="006", name="Priya Sharma", group="A"),
    Student(id="007", name="Omar Khalil", group="A"),
    
    # Group B (7 students)
    Student(id="008", name="Emma Thompson", group="B"),
    Student(id="009", name="Hassan Ali", group="B"),
    Student(id="010", name="Sophie Brown", group="B"),
    Student(id="011", name="Yuki Tanaka", group="B"),
    Student(id="012", name="David Miller", group="B"),
    Student(id="013", name="Layla Abdul", group="B"),
    Student(id="014", name="Ryan O'Connor", group="B"),
    
    # Group C (7 students)  
    Student(id="015", name="Zara Khan", group="C"),
    Student(id="016", name="Tom Wilson", group="C"),
    Student(id="017", name="Aisha Patel", group="C"),
    Student(id="018", name="Lucas Garcia", group="C"),
    Student(id="019", name="Noor Alami", group="C"),
    Student(id="020", name="Jack Smith", group="C"),
    Student(id="021", name="Maya Singh", group="C"),
    
    # Group D (7 students)
    Student(id="022", name="Alex Zhang", group="D"),
    Student(id="023", name="Leila Ibrahim", group="D"),
    Student(id="024", name="Ben Taylor", group="D"),
    Student(id="025", name="Rania Farid", group="D"),
    Student(id="026", name="Sam Davis", group="D"),
    Student(id="027", name="Dina Mansour", group="D"),
    Student(id="028", name="Jake Anderson", group="D"),
]

# --- API Endpoints ---
@app.get("/")
async def root():
    return {"message": "Rubrix Basketball Assessment API"}

@app.get("/basketball/rubric") 
async def get_basketball_rubric():
    return {
        "title": "Year 7 Basketball Assessment",
        "criteria": ["Dribbling", "Passing", "Shooting", "Defense"],
        "students": 28,
        "groups": 4
    }

@app.get("/students")
async def get_all_students():
    """Get all 28 students"""
    return {"students": STUDENTS, "total": len(STUDENTS)}

@app.get("/students/group/{group}")
async def get_students_by_group(group: str):
    """Get students by group (A, B, C, or D)"""
    group_students = [s for s in STUDENTS if s.group.upper() == group.upper()]
    if not group_students:
        raise HTTPException(status_code=404, detail=f"No students found in group {group}")
    return {"group": group.upper(), "students": group_students, "count": len(group_students)}

@app.post("/assessments")
async def create_assessment(assessment: Assessment):
    """Create a new assessment for a student"""
    # Verify student exists
    student = next((s for s in STUDENTS if s.id == assessment.student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Create assessment with ID and timestamp
    assessment_data = {
        "id": str(uuid.uuid4()),
        "student_id": assessment.student_id,
        "student_name": student.name,
        "student_group": student.group,
        "criterion": assessment.criterion,
        "grade": assessment.grade,
        "notes": assessment.notes,
        "timestamp": assessment.timestamp or datetime.now()
    }
    
    assessments_db.append(assessment_data)
    save_assessments(assessments_db)
    return assessment_data

@app.get("/assessments")
async def get_all_assessments():
    """Get all assessments"""
    return {"assessments": assessments_db, "total": len(assessments_db)}

@app.get("/assessments/student/{student_id}")
async def get_student_assessments(student_id: str):
    """Get all assessments for a specific student"""
    student = next((s for s in STUDENTS if s.id == student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student_assessments = [a for a in assessments_db if a["student_id"] == student_id]
    return {
        "student": student,
        "assessments": student_assessments,
        "count": len(student_assessments)
    }

@app.get("/class/summary")
async def get_class_summary():
    """Get class performance summary"""
    if not assessments_db:
        return {
            "total_students": len(STUDENTS),
            "total_assessments": 0,
            "message": "No assessments recorded yet",
            "groups": {"A": 7, "B": 7, "C": 7, "D": 7}
        }
    
    # Calculate statistics
    total_assessments = len(assessments_db)
    avg_grade = sum(a["grade"] for a in assessments_db) / total_assessments
    
    # Group breakdown
    group_stats = {}
    for group in ["A", "B", "C", "D"]:
        group_assessments = [a for a in assessments_db if a["student_group"] == group]
        group_stats[f"group_{group}"] = {
            "total_assessments": len(group_assessments),
            "avg_grade": sum(a["grade"] for a in group_assessments) / len(group_assessments) if group_assessments else 0
        }
    
    return {
        "total_students": len(STUDENTS),
        "total_assessments": total_assessments,
        "class_average": round(avg_grade, 2),
        "group_breakdown": group_stats,
        "criteria_assessed": list(set(a["criterion"] for a in assessments_db))
    }

@app.get("/mobile/lesson/active")
async def get_active_lesson(group: str, criterion: str):
    """Mobile-optimized endpoint for active lesson view."""
    group_students = [s for s in STUDENTS if s.group.upper() == group.upper()]
    if not group_students:
        raise HTTPException(status_code=404, detail=f"No students found in group {group}")

    # Get assessments for the current group and criterion
    assessed_student_ids = {
        a["student_id"] for a in assessments_db 
        if a["student_group"] == group.upper() and a["criterion"].lower() == criterion.lower()
    }

    lesson_status = []
    for student in group_students:
        lesson_status.append({
            "student_id": student.id,
            "name": student.name,
            "assessed": student.id in assessed_student_ids
        })

    return {
        "group": group.upper(),
        "criterion": criterion,
        "students": lesson_status
    }