"""
BIM Vision Pro - Main FastAPI Application
See Your Buildings Differently
IFC files ko analyze karne ke liye backend server with AI
Backend server for analyzing IFC files using AI - BIM Vision Pro
"""

import os
import shutil
from pathlib import Path
from typing import Dict, Any

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ifc_parser import IFCParser
from claude_service import ClaudeService


# FastAPI app initialize karo / Initialize FastAPI app
app = FastAPI(
    title="BIM Vision Pro API",
    description="AI-powered building analysis platform - See Your Buildings Differently | IFC file analysis with intelligent insights",
    version="1.0.0"
)

# CORS middleware setup - sabhi origins se requests allow karo
# CORS middleware - allow requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production mein specific origins use karein
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload folder ka path / Upload folder path
UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)

# Global building data storage (session-based storage)
# Production mein database use karein / Use database in production
building_data_store: Dict[str, Any] = {}


# Request/Response Models
class QuestionRequest(BaseModel):
    """Question request ka model"""
    question: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str


# ============== ENDPOINTS ==============

@app.get("/", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint - server running hai ya nahi check karta hai
    Checks if server is running
    """
    return {
        "status": "ok",
        "message": "BIM Vision Pro API is running successfully! See Your Buildings Differently."
    }


@app.get("/api/test")
async def test_ai_connection():
    """
    OpenAI API connection ko test karta hai
    Tests OpenAI API connection
    """
    try:
        claude_service = ClaudeService()
        return {
            "status": "success",
            "message": "[OK] OpenAI connection successful!",
            "model": claude_service.model
        }
    except ValueError as ve:
        raise HTTPException(
            status_code=400,
            detail=f"API Key error: {str(ve)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Connection test failed: {str(e)}"
        )


@app.post("/api/upload-ifc")
async def upload_ifc_file(file: UploadFile = File(...)):
    """
    IFC file upload karta hai aur uska analysis return karta hai
    Uploads IFC file and returns its analysis

    Args:
        file: IFC file (UploadFile)

    Returns:
        Building data aur Claude AI analysis
    """
    try:
        # File validation - IFC file hai ya nahi check karo
        if not file.filename.lower().endswith('.ifc'):
            raise HTTPException(
                status_code=400,
                detail="[ERROR] Sirf .ifc files allowed hain! / Only .ifc files are allowed!"
            )

        # File ko save karo / Save the file
        file_path = UPLOAD_FOLDER / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"[FILE] File uploaded: {file.filename}")

        # IFC file parse karo / Parse IFC file
        parser = IFCParser()
        parser.load_file(str(file_path))

        # Building data extract karo / Extract building data
        building_data = parser.extract_full_data()

        # Data ko store karo (session ke liye) / Store data for session
        building_data_store["current"] = building_data

        # Claude AI se analysis le lo / Get analysis from Claude AI
        claude_service = ClaudeService()
        analysis = claude_service.analyze_building(building_data)

        print("[OK] Analysis completed successfully")

        # Response return karo / Return response
        return {
            "status": "success",
            "message": "[OK] IFC file successfully analyzed!",
            "filename": file.filename,
            "building_data": building_data,
            "analysis": analysis
        }

    except ValueError as ve:
        # API key error
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        # General error
        print(f"[ERROR] Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"File processing mein error: {str(e)}"
        )

    finally:
        # File cleanup - optional
        # Agar chahein toh file delete kar sakte hain
        # if file_path.exists():
        #     file_path.unlink()
        pass


@app.post("/api/ask-question")
async def ask_question(request: QuestionRequest):
    """
    Building ke baare mein specific question ka answer deta hai
    Answers specific questions about the building

    Args:
        request: QuestionRequest with question field

    Returns:
        Answer from Claude AI
    """
    try:
        # Check karo ki building data available hai ya nahi
        if "current" not in building_data_store:
            raise HTTPException(
                status_code=400,
                detail="[ERROR] Pehle IFC file upload karein! / Please upload an IFC file first!"
            )

        # Question validate karo / Validate question
        if not request.question or request.question.strip() == "":
            raise HTTPException(
                status_code=400,
                detail="[ERROR] Question khali nahi ho sakta! / Question cannot be empty!"
            )

        print(f"[?] Question received: {request.question}")

        # Claude AI se answer le lo / Get answer from Claude AI
        claude_service = ClaudeService()
        answer = claude_service.ask_question(
            building_data_store["current"],
            request.question
        )

        return {
            "status": "success",
            "question": request.question,
            "answer": answer
        }

    except HTTPException:
        raise

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        print(f"[ERROR] Error answering question: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Question answer karne mein error: {str(e)}"
        )


# ============== SERVER START ==============

if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print(">> BIM VISION PRO - Backend Server Starting...")
    print("=" * 60)
    print(">> Server: http://localhost:8000")
    print(">> API Docs: http://localhost:8000/docs")
    print("=" * 60)

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Development mode - auto reload on code changes
    )
