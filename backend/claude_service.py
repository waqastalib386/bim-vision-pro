"""
OpenAI Service - Uses OpenAI for building analysis
"""

import os
from typing import Dict, Any
from openai import OpenAI
from dotenv import load_dotenv
from cache_service import cache_service

# Load environment variables
load_dotenv()


class ClaudeService:
    """
    Class for interacting with OpenAI API
    """

    def __init__(self):
        """
        Initializes the OpenAI client with API key
        """
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key or api_key == "your_openai_api_key_here":
            raise ValueError(
                "[ERROR] OPENAI_API_KEY is not set in .env file!\n"
                "Please add your OpenAI API key in backend/.env file"
            )

        # OpenAI client setup
        self.client = OpenAI(api_key=api_key)
        # Using gpt-4o-mini - fast and good quality
        # Other options: gpt-3.5-turbo (faster, lower quality)
        # Paid models: gpt-4, gpt-4-turbo (require API credits)
        self.model = "gpt-4o-mini"
        print(f"[OK] OpenAI service initialized successfully with model: {self.model}")

    def _create_analysis_prompt(self, building_data: Dict[str, Any]) -> str:
        """
        Creates detailed analysis prompt from building data

        Args:
            building_data: Dictionary with building information

        Returns:
            Formatted prompt string
        """
        project_info = building_data.get("project_info", {})
        elements = building_data.get("element_counts", {})
        materials = building_data.get("materials", [])
        spaces = building_data.get("spaces", [])

        prompt = f"""
You are given BIM (Building Information Modeling) data for a building.
Please provide a detailed analysis in English with professional insights.

[INFO] PROJECT INFORMATION:
- Project Name: {project_info.get('project_name', 'Unknown')}
- Building Name: {project_info.get('building_name', 'Unknown')}
- Description: {project_info.get('description', 'N/A')}

[BUILDING] BUILDING ELEMENTS COUNT:
- Walls: {elements.get('walls', 0)}
- Doors: {elements.get('doors', 0)}
- Windows: {elements.get('windows', 0)}
- Slabs (Floors): {elements.get('slabs', 0)}
- Columns: {elements.get('columns', 0)}
- Beams: {elements.get('beams', 0)}
- Stairs: {elements.get('stairs', 0)}
- Roofs: {elements.get('roofs', 0)}
- Total Elements: {elements.get('total', 0)}

[MATERIALS] MATERIALS USED:
{', '.join(materials) if materials else 'No materials data'}

[SPACES] SPACES/ROOMS:
{len(spaces)} spaces found

Please provide a comprehensive building analysis with the following sections:

1. **Building Overview** - Summary of the building structure and key characteristics
2. **Structural Analysis** - Analysis of structural elements and their distribution
3. **Space Analysis** - Details about rooms, spaces, and spatial organization
4. **Material Analysis** - Insights about materials used and recommendations
5. **Recommendations** - Suggestions for improvements, potential issues, and best practices

Response should be clear, detailed, and professional in English.
"""
        return prompt

    def analyze_building(self, building_data: Dict[str, Any]) -> str:
        """
        Analyzes building data using OpenAI

        Args:
            building_data: Complete building data dictionary

        Returns:
            Analysis result in English
        """
        try:
            # Check cache first for faster response
            data_signature = cache_service.get_data_signature(building_data)
            cached_analysis = cache_service.get_cached_analysis(data_signature)

            if cached_analysis:
                print("[AI] Using cached analysis (super fast!)")
                return cached_analysis

            # Create analysis prompt
            prompt = self._create_analysis_prompt(building_data)

            # Request analysis from OpenAI
            print("[AI] Requesting building analysis from OpenAI...")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=2048,  # Reduced for faster processing
                temperature=0.3  # Lower temperature for faster, more consistent responses
            )

            # Extract response
            analysis = response.choices[0].message.content

            # Cache the analysis for future requests
            cache_service.cache_analysis(data_signature, analysis)

            print("[OK] Building analysis successfully completed")
            return analysis

        except Exception as e:
            error_msg = f"[ERROR] Error in OpenAI analysis: {str(e)}"
            print(error_msg)

            # Provide helpful error messages based on error type
            if "does not exist" in str(e).lower():
                return f"Error: Model '{self.model}' access issue.\n\nPlease check:\n1. API key is valid\n2. Account has credits (check: platform.openai.com/usage)\n3. Model access is available\n\nCurrent model: {self.model}"
            elif "api_key" in str(e).lower() or "authentication" in str(e).lower():
                return "Error: API key is invalid.\n\nPlease set correct OPENAI_API_KEY in backend/.env file."
            elif "rate_limit" in str(e).lower():
                return "Error: Rate limit exceeded.\n\nPlease wait a moment and try again."
            else:
                return f"Error in analysis: {str(e)}\n\nPlease check:\n1. API key is correct (backend/.env)\n2. Internet connection is working\n3. OpenAI account has credits (platform.openai.com/usage)"

    def ask_question(self, building_data: Dict[str, Any], question: str) -> str:
        """
        Answers specific questions about the building

        Args:
            building_data: Complete building data dictionary
            question: User's question

        Returns:
            Answer in English
        """
        try:
            project_info = building_data.get("project_info", {})
            elements = building_data.get("element_counts", {})
            materials = building_data.get("materials", [])
            spaces = building_data.get("spaces", [])

            # Question answering prompt
            prompt = f"""
You are given BIM data for a building and a user has asked a question.
Building data:

[INFO] Project: {project_info.get('project_name', 'Unknown')}
[BUILDING] Building Elements:
- Walls: {elements.get('walls', 0)}
- Doors: {elements.get('doors', 0)}
- Windows: {elements.get('windows', 0)}
- Slabs: {elements.get('slabs', 0)}
- Columns: {elements.get('columns', 0)}
- Beams: {elements.get('beams', 0)}
- Stairs: {elements.get('stairs', 0)}
- Roofs: {elements.get('roofs', 0)}

[MATERIALS] Materials: {', '.join(materials) if materials else 'No data'}
[SPACES] Total Spaces: {len(spaces)}

[USER] USER QUESTION: {question}

Please answer this question in English with detailed and helpful information.
If data is not available, clearly inform the user.
Answer should be professional yet friendly.
"""

            print(f"[AI] Getting answer from OpenAI...")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=2048,
                temperature=0.7
            )

            answer = response.choices[0].message.content

            print("[OK] Question successfully answered")
            return answer

        except Exception as e:
            error_msg = f"[ERROR] Error answering question: {str(e)}"
            print(error_msg)

            # Provide helpful error messages based on error type
            if "does not exist" in str(e).lower():
                return f"Error: Model '{self.model}' access issue.\n\nPlease check:\n1. API key is valid\n2. Account has available credits\n3. Model access is enabled\n\nVisit: platform.openai.com/usage"
            elif "api_key" in str(e).lower() or "authentication" in str(e).lower():
                return "Error: API key is invalid.\n\nPlease check backend/.env file."
            elif "rate_limit" in str(e).lower():
                return "Error: Rate limit exceeded.\n\nPlease wait a moment and try again."
            else:
                return f"Error: {str(e)}\n\nPlease check API key and internet connection.\nCheck credits at: platform.openai.com/usage"


# For testing
if __name__ == "__main__":
    print("OpenAI Service module loaded successfully")
    print("Note: API key must be set in .env file")
