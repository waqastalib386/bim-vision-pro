"""
BIM Vision Pro - Main FastAPI Application
See Your Buildings Differently
IFC files ko analyze karne ke liye backend server with AI
Backend server for analyzing IFC files using AI - BIM Vision Pro
"""

import os
import shutil
import time
import traceback
from pathlib import Path
from typing import Dict, Any, Optional

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ifc_parser import IFCParser
from claude_service import ClaudeService
from supabase_service import SupabaseService


# FastAPI app initialize karo / Initialize FastAPI app
app = FastAPI(
    title="BIM Vision Pro API",
    description="AI-powered building analysis platform - See Your Buildings Differently | IFC file analysis with intelligent insights",
    version="1.0.0"
)

# CORS middleware setup - specific origins allow karo for production
# CORS middleware - allow requests from specific origins for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://bimvisionpro.netlify.app",
        "https://*.netlify.app",  # Allow all Netlify preview URLs
        "http://localhost:3000",  # Vite dev server
        "http://localhost:5173",  # Alternate Vite port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload folder ka path / Upload folder path
UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)

# Global building data storage (session-based storage)
# Also stored in Supabase database for persistence
building_data_store: Dict[str, Any] = {}

# Initialize Supabase service (with error handling)
supabase_service: Optional[SupabaseService] = None
try:
    supabase_service = SupabaseService()
    print("[OK] Supabase integration enabled")
except Exception as e:
    print(f"[WARNING] Supabase not available: {str(e)}")
    print("[INFO] App will continue without database persistence")


# Request/Response Models
class QuestionRequest(BaseModel):
    """Question request ka model"""
    question: str
    analysis_id: Optional[str] = None  # For linking Q&A to specific analysis
    user_id: Optional[str] = "anonymous"


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
async def upload_ifc_file(
    file: UploadFile = File(...),
    user_id: str = "anonymous"
):
    """
    IFC file upload karta hai aur uska analysis return karta hai
    Uploads IFC file and returns its analysis

    Args:
        file: IFC file (UploadFile)
        user_id: User identifier (default: "anonymous")

    Returns:
        Building data, AI analysis, and analysis_id
    """
    start_time = time.time()
    file_size = 0
    analysis_id = None

    try:
        # File validation - IFC file hai ya nahi check karo
        if not file.filename.lower().endswith('.ifc'):
            raise HTTPException(
                status_code=400,
                detail="[ERROR] Sirf .ifc files allowed hain! / Only .ifc files are allowed!"
            )

        # File ko save karo aur size track karo / Save file and track size
        file_path = UPLOAD_FOLDER / file.filename
        with open(file_path, "wb") as buffer:
            content = await file.read()
            file_size = len(content)
            buffer.write(content)

        print(f"[FILE] File uploaded: {file.filename} ({file_size} bytes)")

        # IFC file parse karo / Parse IFC file
        parser = IFCParser()
        parser.load_file(str(file_path))

        # Building data extract karo / Extract building data
        building_data = parser.extract_full_data()

        # Claude AI se analysis le lo / Get analysis from OpenAI
        claude_service = ClaudeService()
        analysis = claude_service.analyze_building(building_data)

        # Calculate processing time
        processing_time = time.time() - start_time

        # Store in Supabase database (if available)
        if supabase_service:
            try:
                analysis_id = supabase_service.store_analysis_result(
                    filename=file.filename,
                    building_data=building_data,
                    ai_analysis=analysis,
                    user_id=user_id,
                    processing_time=processing_time,
                    file_size=file_size
                )
                print(f"[DB] Analysis stored in Supabase: {analysis_id}")
            except Exception as db_error:
                print(f"[WARNING] Failed to store in Supabase: {str(db_error)}")
                # Continue even if database storage fails

        # Data ko store karo (session ke liye) / Store data for session
        building_data_store["current"] = building_data
        building_data_store["current_analysis_id"] = analysis_id

        print(f"[OK] Analysis completed successfully in {processing_time:.2f}s")

        # Response return karo / Return response
        return {
            "status": "success",
            "message": "[OK] IFC file successfully analyzed!",
            "filename": file.filename,
            "analysis_id": analysis_id,
            "file_size": file_size,
            "processing_time": processing_time,
            "building_data": building_data,
            "analysis": analysis
        }

    except ValueError as ve:
        # API key error
        print(f"[ERROR] ValueError in upload endpoint: {str(ve)}")
        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        # General error - detailed logging for debugging
        print(f"[ERROR] Exception in upload endpoint: {str(e)}")
        print(f"[ERROR] Exception type: {type(e).__name__}")
        print(f"[ERROR] File details - filename: {file.filename if file else 'N/A'}, content_type: {file.content_type if file else 'N/A'}")
        print(f"[ERROR] Full traceback:\n{traceback.format_exc()}")
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
        request: QuestionRequest with question, analysis_id (optional), user_id (optional)

    Returns:
        Answer from OpenAI
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

        # OpenAI se answer le lo / Get answer from OpenAI
        claude_service = ClaudeService()
        answer = claude_service.ask_question(
            building_data_store["current"],
            request.question
        )

        # Store Q&A in Supabase (if available)
        if supabase_service:
            try:
                # Get analysis_id from request or from current session
                analysis_id = request.analysis_id or building_data_store.get("current_analysis_id")

                if analysis_id:
                    supabase_service.store_qa_interaction(
                        analysis_id=analysis_id,
                        question=request.question,
                        answer=answer,
                        user_id=request.user_id or "anonymous"
                    )
                    print(f"[DB] Q&A stored in Supabase for analysis: {analysis_id}")
            except Exception as db_error:
                print(f"[WARNING] Failed to store Q&A in Supabase: {str(db_error)}")
                # Continue even if database storage fails

        return {
            "status": "success",
            "question": request.question,
            "answer": answer,
            "analysis_id": request.analysis_id or building_data_store.get("current_analysis_id")
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


@app.get("/api/history/{user_id}")
async def get_user_history(
    user_id: str,
    limit: int = 50,
    offset: int = 0
):
    """
    Get user's analysis history from database

    Args:
        user_id: User identifier
        limit: Maximum number of results (default: 50)
        offset: Number of results to skip (default: 0)

    Returns:
        List of past analyses
    """
    if not supabase_service:
        raise HTTPException(
            status_code=503,
            detail="[ERROR] Database service not available"
        )

    try:
        analyses = supabase_service.get_user_analyses(
            user_id=user_id,
            limit=limit,
            offset=offset
        )

        return {
            "status": "success",
            "user_id": user_id,
            "count": len(analyses),
            "analyses": analyses
        }

    except Exception as e:
        print(f"[ERROR] Failed to retrieve history: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"History retrieve karne mein error: {str(e)}"
        )


@app.get("/api/analysis/{analysis_id}")
async def get_analysis(analysis_id: str):
    """
    Get specific analysis by ID

    Args:
        analysis_id: Analysis ID

    Returns:
        Complete analysis data with Q&A history
    """
    if not supabase_service:
        raise HTTPException(
            status_code=503,
            detail="[ERROR] Database service not available"
        )

    try:
        # Get analysis data
        analysis = supabase_service.get_analysis_by_id(analysis_id)

        if not analysis:
            raise HTTPException(
                status_code=404,
                detail=f"[ERROR] Analysis not found: {analysis_id}"
            )

        # Get Q&A history
        qa_history = supabase_service.get_qa_history(analysis_id)

        return {
            "status": "success",
            "analysis": analysis,
            "qa_history": qa_history,
            "qa_count": len(qa_history)
        }

    except HTTPException:
        raise

    except Exception as e:
        print(f"[ERROR] Failed to retrieve analysis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis retrieve karne mein error: {str(e)}"
        )


@app.delete("/api/analysis/{analysis_id}")
async def delete_analysis(analysis_id: str):
    """
    Delete analysis and associated Q&A history

    Args:
        analysis_id: Analysis ID to delete

    Returns:
        Success confirmation
    """
    if not supabase_service:
        raise HTTPException(
            status_code=503,
            detail="[ERROR] Database service not available"
        )

    try:
        success = supabase_service.delete_analysis(analysis_id)

        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"[ERROR] Analysis not found or could not be deleted: {analysis_id}"
            )

        return {
            "status": "success",
            "message": f"Analysis deleted successfully: {analysis_id}"
        }

    except HTTPException:
        raise

    except Exception as e:
        print(f"[ERROR] Failed to delete analysis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis delete karne mein error: {str(e)}"
        )


@app.get("/api/stats/{user_id}")
async def get_user_stats(user_id: str):
    """
    Get user statistics

    Args:
        user_id: User identifier

    Returns:
        User statistics (total analyses, last active, etc.)
    """
    if not supabase_service:
        raise HTTPException(
            status_code=503,
            detail="[ERROR] Database service not available"
        )

    try:
        stats = supabase_service.get_user_statistics(user_id)

        if not stats:
            return {
                "status": "success",
                "user_id": user_id,
                "message": "No statistics available",
                "total_analyses": 0
            }

        return {
            "status": "success",
            "user_id": user_id,
            "statistics": stats
        }

    except Exception as e:
        print(f"[ERROR] Failed to retrieve statistics: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Statistics retrieve karne mein error: {str(e)}"
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
