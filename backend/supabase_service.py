"""
Supabase Service - Database operations for BIM Vision Pro
Handles storing and retrieving analysis results, Q&A history, and user sessions
"""

import os
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class SupabaseService:
    """
    Supabase service for database operations
    Manages analysis results, Q&A history, and user statistics
    """

    def __init__(self):
        """
        Initialize Supabase client with credentials from environment variables
        """
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")

        if not supabase_url or supabase_url == "https://your-project.supabase.co":
            raise ValueError(
                "[ERROR] SUPABASE_URL not set in .env file!\n"
                "Please add your Supabase URL in backend/.env file"
            )

        if not supabase_key or supabase_key == "your_supabase_anon_key_here":
            raise ValueError(
                "[ERROR] SUPABASE_KEY not set in .env file!\n"
                "Please add your Supabase key in backend/.env file"
            )

        try:
            self.client: Client = create_client(supabase_url, supabase_key)
            print("[OK] Supabase service initialized successfully")
        except Exception as e:
            print(f"[ERROR] Failed to initialize Supabase client: {str(e)}")
            raise

    def store_analysis_result(
        self,
        filename: str,
        building_data: Dict[str, Any],
        ai_analysis: str,
        user_id: str = "anonymous",
        processing_time: float = 0.0,
        file_size: int = 0
    ) -> Optional[str]:
        """
        Store IFC analysis result in database

        Args:
            filename: Name of the IFC file
            building_data: Complete building data dictionary
            ai_analysis: AI-generated analysis text
            user_id: User identifier (default: "anonymous")
            processing_time: Time taken to process (seconds)
            file_size: Size of uploaded file (bytes)

        Returns:
            Analysis ID if successful, None if failed
        """
        try:
            analysis_id = str(uuid.uuid4())
            project_info = building_data.get("project_info", {})
            element_counts = building_data.get("element_counts", {})
            validation = building_data.get("validation", {})
            costing = building_data.get("costing", {})

            # Prepare data for insertion
            data = {
                "id": analysis_id,
                "user_id": user_id,
                "filename": filename,
                "file_size": file_size,
                "project_name": project_info.get("project_name", "Unknown"),
                "building_name": project_info.get("building_name", "Unknown"),
                "description": project_info.get("description", ""),
                "total_elements": element_counts.get("total", 0),
                "walls_count": element_counts.get("walls", 0),
                "doors_count": element_counts.get("doors", 0),
                "windows_count": element_counts.get("windows", 0),
                "slabs_count": element_counts.get("slabs", 0),
                "columns_count": element_counts.get("columns", 0),
                "beams_count": element_counts.get("beams", 0),
                "stairs_count": element_counts.get("stairs", 0),
                "roofs_count": element_counts.get("roofs", 0),
                "materials": building_data.get("materials", []),
                "spaces": building_data.get("spaces", []),
                "ai_analysis": ai_analysis,
                "validation_errors": validation.get("errors", []),
                "validation_warnings": validation.get("warnings", []),
                "total_cost": costing.get("total_cost", 0.0),
                "cost_breakdown": costing.get("breakdown", {}),
                "processing_time": processing_time,
                "created_at": datetime.utcnow().isoformat()
            }

            # Insert into analysis_results table
            result = self.client.table("analysis_results").insert(data).execute()

            print(f"[OK] Analysis result stored in Supabase: {analysis_id}")

            # Update user session statistics
            self._update_user_session(user_id)

            return analysis_id

        except Exception as e:
            print(f"[ERROR] Failed to store analysis result: {str(e)}")
            return None

    def store_qa_interaction(
        self,
        analysis_id: str,
        question: str,
        answer: str,
        user_id: str = "anonymous"
    ) -> bool:
        """
        Store question and answer interaction

        Args:
            analysis_id: ID of the analysis this Q&A belongs to
            question: User's question
            answer: AI's answer
            user_id: User identifier

        Returns:
            True if successful, False otherwise
        """
        try:
            qa_id = str(uuid.uuid4())

            data = {
                "id": qa_id,
                "analysis_id": analysis_id,
                "user_id": user_id,
                "question": question,
                "answer": answer,
                "created_at": datetime.utcnow().isoformat()
            }

            # Insert into qa_history table
            self.client.table("qa_history").insert(data).execute()

            print(f"[OK] Q&A interaction stored: {qa_id}")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to store Q&A interaction: {str(e)}")
            return False

    def get_user_analyses(
        self,
        user_id: str = "anonymous",
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Retrieve user's past analyses

        Args:
            user_id: User identifier
            limit: Maximum number of results
            offset: Number of results to skip

        Returns:
            List of analysis dictionaries
        """
        try:
            result = (
                self.client.table("analysis_results")
                .select("*")
                .eq("user_id", user_id)
                .order("created_at", desc=True)
                .range(offset, offset + limit - 1)
                .execute()
            )

            print(f"[OK] Retrieved {len(result.data)} analyses for user: {user_id}")
            return result.data

        except Exception as e:
            print(f"[ERROR] Failed to retrieve user analyses: {str(e)}")
            return []

    def get_analysis_by_id(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """
        Get specific analysis by ID

        Args:
            analysis_id: Analysis ID

        Returns:
            Analysis dictionary if found, None otherwise
        """
        try:
            result = (
                self.client.table("analysis_results")
                .select("*")
                .eq("id", analysis_id)
                .single()
                .execute()
            )

            print(f"[OK] Retrieved analysis: {analysis_id}")
            return result.data

        except Exception as e:
            print(f"[ERROR] Failed to retrieve analysis: {str(e)}")
            return None

    def get_qa_history(
        self,
        analysis_id: str,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get Q&A history for a specific analysis

        Args:
            analysis_id: Analysis ID
            limit: Maximum number of results

        Returns:
            List of Q&A dictionaries
        """
        try:
            result = (
                self.client.table("qa_history")
                .select("*")
                .eq("analysis_id", analysis_id)
                .order("created_at", desc=False)
                .limit(limit)
                .execute()
            )

            print(f"[OK] Retrieved {len(result.data)} Q&A interactions for analysis: {analysis_id}")
            return result.data

        except Exception as e:
            print(f"[ERROR] Failed to retrieve Q&A history: {str(e)}")
            return []

    def delete_analysis(self, analysis_id: str) -> bool:
        """
        Delete analysis and associated Q&A history

        Args:
            analysis_id: Analysis ID to delete

        Returns:
            True if successful, False otherwise
        """
        try:
            # Delete Q&A history first (foreign key constraint)
            self.client.table("qa_history").delete().eq("analysis_id", analysis_id).execute()

            # Delete analysis result
            self.client.table("analysis_results").delete().eq("id", analysis_id).execute()

            print(f"[OK] Deleted analysis and Q&A history: {analysis_id}")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to delete analysis: {str(e)}")
            return False

    def _update_user_session(self, user_id: str) -> None:
        """
        Update or create user session statistics

        Args:
            user_id: User identifier
        """
        try:
            # Check if user session exists
            result = (
                self.client.table("user_sessions")
                .select("*")
                .eq("user_id", user_id)
                .execute()
            )

            if result.data:
                # Update existing session
                current_count = result.data[0].get("total_analyses", 0)
                self.client.table("user_sessions").update({
                    "total_analyses": current_count + 1,
                    "last_active": datetime.utcnow().isoformat()
                }).eq("user_id", user_id).execute()
            else:
                # Create new session
                session_id = str(uuid.uuid4())
                self.client.table("user_sessions").insert({
                    "id": session_id,
                    "user_id": user_id,
                    "total_analyses": 1,
                    "last_active": datetime.utcnow().isoformat(),
                    "created_at": datetime.utcnow().isoformat()
                }).execute()

            print(f"[OK] Updated user session: {user_id}")

        except Exception as e:
            print(f"[ERROR] Failed to update user session: {str(e)}")

    def get_user_statistics(self, user_id: str = "anonymous") -> Optional[Dict[str, Any]]:
        """
        Get user statistics

        Args:
            user_id: User identifier

        Returns:
            User statistics dictionary if found, None otherwise
        """
        try:
            result = (
                self.client.table("user_sessions")
                .select("*")
                .eq("user_id", user_id)
                .single()
                .execute()
            )

            print(f"[OK] Retrieved user statistics: {user_id}")
            return result.data

        except Exception as e:
            print(f"[ERROR] Failed to retrieve user statistics: {str(e)}")
            return None


# Testing
if __name__ == "__main__":
    print("Supabase Service module loaded successfully")
    print("Note: Supabase credentials must be set in .env file")
