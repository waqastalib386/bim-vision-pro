"""
BIM Vision Pro - Main FastAPI Application
See Your Buildings Differently
Backend server for analyzing IFC files using AI
"""

import os
import shutil
import time
import traceback
import asyncio
import httpx
from pathlib import Path
from typing import Dict, Any, Optional

from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ifc_parser import IFCParser
from claude_service import ClaudeService
from supabase_service import SupabaseService
from cache_service import cache_service


# Initialize FastAPI app
app = FastAPI(
    title="BIM Vision Pro API",
    description="AI-powered building analysis platform - See Your Buildings Differently | IFC file analysis with intelligent insights",
    version="1.0.0"
)

# CORS middleware setup - allow Netlify and localhost origins
# CORS middleware - allow requests from production and development
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.netlify\.app",  # Allows all Netlify subdomains
    allow_origins=[
        "https://bimvisionpro.netlify.app",  # Main production domain
        "http://localhost:3000",  # Vite dev server
        "http://localhost:5173",  # Alternate Vite port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Performance monitoring middleware
@app.middleware("http")
async def add_performance_metrics(request: Request, call_next):
    """Track request processing time for performance monitoring"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.3f}s"

    # Log slow requests
    if process_time > 5.0:
        print(f"[PERF] SLOW REQUEST: {request.url.path} took {process_time:.2f}s")
    else:
        print(f"[PERF] {request.url.path} processed in {process_time:.3f}s")

    return response

# Upload folder path
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
    """Question request model"""
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
    Health check endpoint - checks if server is running
    """
    return {
        "status": "ok",
        "message": "BIM Vision Pro API is running successfully! See Your Buildings Differently."
    }


@app.get("/api/cache-stats")
async def get_cache_stats():
    """
    Get cache statistics for performance monitoring
    """
    return {
        "status": "success",
        "cache_stats": cache_service.get_cache_stats()
    }


@app.get("/api/test")
async def test_ai_connection():
    """
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
        # File validation - check if IFC file
        if not file.filename.lower().endswith('.ifc'):
            raise HTTPException(
                status_code=400,
                detail="[ERROR] Only .ifc files are allowed!"
            )

        # Read file content
        content = await file.read()
        file_size = len(content)
        file_size_mb = file_size / (1024 * 1024)

        print(f"[FILE] Receiving file: {file.filename}")
        print(f"[FILE] Size: {file_size_mb:.2f} MB")

        # Check file size limit (500MB max)
        MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"[ERROR] File too large! Maximum size is 500MB. Your file is {file_size_mb:.2f} MB"
            )

        # Check cache using file hash for super fast response
        file_hash = cache_service.get_file_hash(content)
        cached_data = cache_service.get_cached_file_data(file_hash)

        if cached_data:
            # File already processed - instant response!
            print(f"[CACHE] File already processed! Returning cached results (instant)")
            processing_time = time.time() - start_time

            return {
                "status": "success",
                "message": "[OK] IFC file successfully analyzed (from cache)!",
                "filename": file.filename,
                "analysis_id": None,
                "file_size": file_size,
                "processing_time": processing_time,
                "cached": True,
                "building_data": cached_data["building_data"],
                "analysis": cached_data["analysis"]
            }

        # New file - process it
        file_path = UPLOAD_FOLDER / file.filename
        with open(file_path, "wb") as buffer:
            buffer.write(content)

        print(f"[FILE] File uploaded: {file.filename} ({file_size} bytes)")

        # Parse IFC file
        parser = IFCParser()
        parser.load_file(str(file_path))

        # Extract building data
        building_data = parser.extract_full_data()

        # Get analysis from OpenAI
        claude_service = ClaudeService()
        analysis = claude_service.analyze_building(building_data)

        # Cache the results for future requests
        cache_service.cache_file_data(file_hash, {
            "building_data": building_data,
            "analysis": analysis
        })

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

        # Store data for session
        building_data_store["current"] = building_data
        building_data_store["current_analysis_id"] = analysis_id

        print(f"[OK] Analysis completed successfully in {processing_time:.2f}s")

        # Return response
        return {
            "status": "success",
            "message": "[OK] IFC file successfully analyzed!",
            "filename": file.filename,
            "analysis_id": analysis_id,
            "file_size": file_size,
            "processing_time": processing_time,
            "cached": False,
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
            detail=f"Error processing file: {str(e)}"
        )

    finally:
        # File cleanup - optional
        # Can delete file if desired
        # if file_path.exists():
        #     file_path.unlink()
        pass


@app.post("/api/ask-question")
async def ask_question(request: QuestionRequest):
    """
    Answers specific questions about the building

    Args:
        request: QuestionRequest with question, analysis_id (optional), user_id (optional)

    Returns:
        Answer from OpenAI
    """
    try:
        # Check if building data is available
        if "current" not in building_data_store:
            raise HTTPException(
                status_code=400,
                detail="[ERROR] Please upload an IFC file first!"
            )

        # Validate question
        if not request.question or request.question.strip() == "":
            raise HTTPException(
                status_code=400,
                detail="[ERROR] Question cannot be empty!"
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
            detail=f"Error answering question: {str(e)}"
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
            detail=f"Error retrieving history: {str(e)}"
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
            detail=f"Error retrieving analysis: {str(e)}"
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
            detail=f"Error deleting analysis: {str(e)}"
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
            detail=f"Error retrieving statistics: {str(e)}"
        )


# ============== KEEP-ALIVE MECHANISM ==============

keep_alive_task = None


async def keep_alive_ping():
    """
    Keep-alive mechanism to prevent Render cold starts
    Pings itself every 8 minutes to keep server warm
    """
    # Wait 60 seconds before starting pings (let server fully start)
    await asyncio.sleep(60)

    print("[KEEP-ALIVE] Keep-alive mechanism started (ping every 8 minutes)")

    while True:
        try:
            await asyncio.sleep(480)  # 8 minutes = 480 seconds (before 10min timeout)

            # Self-ping to keep server alive
            async with httpx.AsyncClient(timeout=15.0) as client:
                # Try to determine the deployment URL
                deployment_url = os.getenv("RENDER_EXTERNAL_URL")
                if deployment_url:
                    url = f"{deployment_url}/api/cache-stats"
                    print(f"[KEEP-ALIVE] Pinging production server...")
                    response = await client.get(url)
                    if response.status_code == 200:
                        print(f"[KEEP-ALIVE] ✅ Ping successful - server staying warm")
                        cache_stats = response.json().get("cache_stats", {})
                        print(f"[KEEP-ALIVE] Cache: {cache_stats}")
                    else:
                        print(f"[KEEP-ALIVE] ⚠️ Ping returned status {response.status_code}")
                else:
                    print(f"[KEEP-ALIVE] ℹ️ Local development - skipping ping")

        except Exception as e:
            print(f"[KEEP-ALIVE] ⚠️ Ping failed: {str(e)}")


@app.on_event("startup")
async def startup_event():
    """Start keep-alive task when server starts"""
    global keep_alive_task

    # Only enable keep-alive in production (Render)
    if os.getenv("RENDER_EXTERNAL_URL"):
        keep_alive_task = asyncio.create_task(keep_alive_ping())
        print("[KEEP-ALIVE] Keep-alive enabled for production deployment")
    else:
        print("[INFO] Keep-alive disabled (local development)")

    print("[STARTUP] Server startup complete")
    print(f"[CACHE] Cache service ready: {cache_service.get_cache_stats()}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on server shutdown"""
    global keep_alive_task

    if keep_alive_task:
        keep_alive_task.cancel()
        print("[KEEP-ALIVE] Keep-alive task cancelled")

    print("[SHUTDOWN] Server shutting down")


# ============== SERVER START ==============

if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print(">> BIM VISION PRO - Backend Server Starting...")
    print("=" * 60)
    print(">> Server: http://localhost:8000")
    print(">> API Docs: http://localhost:8000/docs")
    print(">> Max file size: 500MB")
    print(">> Timeout: 5 minutes")
    print("=" * 60)

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Development mode - auto reload on code changes
        timeout_keep_alive=300,  # 5 minutes timeout for large files
        limit_max_requests=1000,
        limit_concurrency=50
    )
