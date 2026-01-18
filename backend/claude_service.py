"""
OpenAI Service - Building analysis ke liye OpenAI ka use karta hai
Uses OpenAI for building analysis
"""

import os
from typing import Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

# Environment variables load karo / Load environment variables
load_dotenv()


class ClaudeService:
    """
    OpenAI ke saath interact karne ka class
    Class for interacting with OpenAI API
    """

    def __init__(self):
        """
        OpenAI client ko initialize karta hai
        Initializes the OpenAI client with API key
        """
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key or api_key == "your_openai_api_key_here":
            raise ValueError(
                "[ERROR] OPENAI_API_KEY .env file mein set nahi hai!\n"
                "Please add your OpenAI API key in backend/.env file"
            )

        # OpenAI client setup
        self.client = OpenAI(api_key=api_key)
        # Using gpt-4o-mini (free tier model) - fast and good quality
        # Other options: gpt-3.5-turbo (faster, lower quality)
        # Paid models: gpt-4, gpt-4-turbo (require API credits)
        self.model = "gpt-4o-mini"
        print(f"[OK] OpenAI service initialized successfully with model: {self.model}")

    def _create_analysis_prompt(self, building_data: Dict[str, Any]) -> str:
        """
        Building data se detailed analysis prompt banata hai
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
Aapko ek building ka BIM (Building Information Modeling) data diya gaya hai.
Iska detailed analysis Hindi-English mix (Hinglish) mein provide karo.

[INFO] PROJECT INFORMATION:
- Project Name: {project_info.get('project_name', 'Unknown')}
- Building Name: {project_info.get('building_name', 'Unknown')}
- Description: {project_info.get('description', 'N/A')}

[BUILDING] BUILDING ELEMENTS COUNT:
- Walls (Deewaren): {elements.get('walls', 0)}
- Doors (Darwaze): {elements.get('doors', 0)}
- Windows (Khidkiyan): {elements.get('windows', 0)}
- Slabs (Floor Slabs): {elements.get('slabs', 0)}
- Columns (Khambe): {elements.get('columns', 0)}
- Beams: {elements.get('beams', 0)}
- Stairs (Seedhiyan): {elements.get('stairs', 0)}
- Roofs (Chhatein): {elements.get('roofs', 0)}
- Total Elements: {elements.get('total', 0)}

[MATERIALS] MATERIALS USED:
{', '.join(materials) if materials else 'No materials data'}

[SPACES] SPACES/ROOMS:
{len(spaces)} spaces found

Kripya is building ka analysis Hinglish mein provide karo with following sections:

1. **Building Overview** - Building ke baare mein summary
2. **Structural Analysis** - Structural elements ka analysis
3. **Space Analysis** - Rooms aur spaces ki details
4. **Material Analysis** - Materials ke baare mein insights
5. **Recommendations** - Improvement ke liye suggestions

Response clear, detailed aur Hinglish mein hona chahiye!
"""
        return prompt

    def analyze_building(self, building_data: Dict[str, Any]) -> str:
        """
        Building data ko OpenAI se analyze karta hai
        Analyzes building data using OpenAI

        Args:
            building_data: Complete building data dictionary

        Returns:
            Analysis result in Hinglish
        """
        try:
            # Analysis prompt create karo / Create analysis prompt
            prompt = self._create_analysis_prompt(building_data)

            # OpenAI se analysis request karo / Request analysis from OpenAI
            print("[AI] OpenAI se building analysis request kar rahe hain...")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=4096,
                temperature=0.7
            )

            # Response extract karo / Extract response
            analysis = response.choices[0].message.content

            print("[OK] Building analysis successfully completed")
            return analysis

        except Exception as e:
            error_msg = f"[ERROR] OpenAI analysis mein error: {str(e)}"
            print(error_msg)

            # Provide helpful error messages based on error type
            if "does not exist" in str(e).lower():
                return f"Error: Model '{self.model}' access issue.\n\nKripya check karein:\n1. API key sahi hai\n2. Account mein credits hain (check: platform.openai.com/usage)\n3. Model access available hai\n\nCurrent model: {self.model}"
            elif "api_key" in str(e).lower() or "authentication" in str(e).lower():
                return "Error: API key invalid hai.\n\nKripya backend/.env file mein sahi OPENAI_API_KEY set karein."
            elif "rate_limit" in str(e).lower():
                return "Error: Rate limit exceed ho gaya.\n\nKuch der wait karein aur phir try karein."
            else:
                return f"Error in analysis: {str(e)}\n\nKripya check karein:\n1. API key sahi hai (backend/.env)\n2. Internet connection working hai\n3. OpenAI account mein credits hain (platform.openai.com/usage)"

    def ask_question(self, building_data: Dict[str, Any], question: str) -> str:
        """
        Building ke baare mein specific question ka answer deta hai
        Answers specific questions about the building

        Args:
            building_data: Complete building data dictionary
            question: User ka question

        Returns:
            Answer in Hinglish
        """
        try:
            project_info = building_data.get("project_info", {})
            elements = building_data.get("element_counts", {})
            materials = building_data.get("materials", [])
            spaces = building_data.get("spaces", [])

            # Question answering prompt / Question ka prompt banao
            prompt = f"""
Aapko ek building ka BIM data diya gaya hai aur user ne ek question pucha hai.
Building ka data:

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

Kripya is question ka answer Hinglish (Hindi-English mix) mein detailed aur helpful tareeke se do.
Agar data available nahi hai toh user ko clearly batao.
Answer professional but friendly hona chahiye.
"""

            print(f"[AI] Question ka answer OpenAI se le rahe hain...")

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
            error_msg = f"[ERROR] Question answer karne mein error: {str(e)}"
            print(error_msg)

            # Provide helpful error messages based on error type
            if "does not exist" in str(e).lower():
                return f"Error: Model '{self.model}' access issue.\n\nKripya check karein:\n1. API key valid hai\n2. Account credits available hain\n3. Model access hai\n\nVisit: platform.openai.com/usage"
            elif "api_key" in str(e).lower() or "authentication" in str(e).lower():
                return "Error: API key invalid hai.\n\nKripya backend/.env file check karein."
            elif "rate_limit" in str(e).lower():
                return "Error: Rate limit exceed ho gaya.\n\nThodi der wait karein."
            else:
                return f"Error: {str(e)}\n\nKripya API key aur internet connection check karein.\nCredits check karein: platform.openai.com/usage"


# Testing ke liye / For testing
if __name__ == "__main__":
    print("OpenAI Service module loaded successfully")
    print("Note: API key .env file mein set karna zaruri hai")
