"""
IFC Parser - Extracts building data from IFC files using ifcopenshell
"""

import ifcopenshell
from typing import Dict, List, Optional, Any


class IFCParser:
    """
    Main class for parsing IFC files
    """

    def __init__(self):
        """Initialize parser"""
        self.ifc_file = None
        self.file_path = None

    def load_file(self, file_path: str) -> bool:
        """
        Loads the IFC file

        Args:
            file_path: Path to IFC file

        Returns:
            bool: Success or failure
        """
        try:
            self.file_path = file_path
            self.ifc_file = ifcopenshell.open(file_path)
            print(f"[OK] IFC file successfully loaded: {file_path}")
            return True
        except Exception as e:
            print(f"[ERROR] Error loading IFC file: {str(e)}")
            raise Exception(f"Failed to load IFC file: {str(e)}")

    def get_project_info(self) -> Dict[str, str]:
        """
        Project aur building basic information extracts
        Extracts basic project and building information

        Returns:
            Dict with project_name, building_name, description
        """
        try:
            info = {
                "project_name": "Unknown",
                "building_name": "Unknown",
                "description": "No description available"
            }

            # Project info nikalo / Get project info
            projects = self.ifc_file.by_type("IfcProject")
            if projects:
                project = projects[0]
                info["project_name"] = project.Name or "Unknown Project"
                info["description"] = project.Description or "No description"

            # Building info nikalo / Get building info
            buildings = self.ifc_file.by_type("IfcBuilding")
            if buildings:
                building = buildings[0]
                info["building_name"] = building.Name or "Unknown Building"

            return info

        except Exception as e:
            print(f"[ERROR] Error getting project info: {str(e)}")
            return {
                "project_name": "Error",
                "building_name": "Error",
                "description": f"Error: {str(e)}"
            }

    def count_elements(self) -> Dict[str, int]:
        """
        Building elements the count does
        Counts building elements (walls, doors, windows, etc.)

        Returns:
            Dict with counts of different elements
        """
        try:
            elements = {
                "walls": len(self.ifc_file.by_type("IfcWall")),
                "doors": len(self.ifc_file.by_type("IfcDoor")),
                "windows": len(self.ifc_file.by_type("IfcWindow")),
                "slabs": len(self.ifc_file.by_type("IfcSlab")),
                "columns": len(self.ifc_file.by_type("IfcColumn")),
                "beams": len(self.ifc_file.by_type("IfcBeam")),
                "stairs": len(self.ifc_file.by_type("IfcStair")),
                "roofs": len(self.ifc_file.by_type("IfcRoof")),
            }

            # Total elements count karo / Calculate total
            elements["total"] = sum(elements.values())

            return elements

        except Exception as e:
            print(f"[ERROR] Error counting elements: {str(e)}")
            return {
                "walls": 0, "doors": 0, "windows": 0, "slabs": 0,
                "columns": 0, "beams": 0, "stairs": 0, "roofs": 0,
                "total": 0
            }

    def get_materials(self) -> List[str]:
        """
        Building in use hue materials list extracts
        Extracts list of materials used in the building

        Returns:
            List of material names
        """
        try:
            materials = []
            material_elements = self.ifc_file.by_type("IfcMaterial")

            for material in material_elements:
                if hasattr(material, 'Name') and material.Name:
                    materials.append(material.Name)

            # Duplicate materials the remove karo / Remove duplicates
            materials = list(set(materials))

            return materials if materials else ["No materials found"]

        except Exception as e:
            print(f"[ERROR] Error getting materials: {str(e)}")
            return [f"Error: {str(e)}"]

    def get_spaces(self) -> List[Dict[str, Any]]:
        """
        Building ke rooms/spaces information extracts
        Extracts room/space information

        Returns:
            List of spaces with their details
        """
        try:
            spaces_list = []
            spaces = self.ifc_file.by_type("IfcSpace")

            for space in spaces:
                space_info = {
                    "name": space.Name or "Unnamed Space",
                    "long_name": space.LongName or "No description",
                    "type": "Space"
                }
                spaces_list.append(space_info)

            return spaces_list if spaces_list else [{"name": "No spaces found", "long_name": "N/A", "type": "N/A"}]

        except Exception as e:
            print(f"[ERROR] Error getting spaces: {str(e)}")
            return [{"name": "Error", "long_name": str(e), "type": "Error"}]

    def validate_ifc_file(self) -> Dict[str, Any]:
        """
        IFC file validation does aur errors detect does
        Validates IFC file and detects errors and missing elements

        Returns:
            Dict with validation results, errors, warnings, and missing elements
        """
        try:
            validation_results = {
                "is_valid": True,
                "errors": [],
                "warnings": [],
                "missing_elements": [],
                "recommendations": []
            }

            # Check 1: Basic project info validation
            project_info = self.get_project_info()
            if project_info.get("project_name") == "Unknown Project":
                validation_results["warnings"].append({
                    "type": "Missing Project Name",
                    "location": "IfcProject",
                    "message": "Project name missing is. Ye mandatory information is.",
                    "severity": "medium"
                })

            if project_info.get("building_name") == "Unknown Building":
                validation_results["warnings"].append({
                    "type": "Missing Building Name",
                    "location": "IfcBuilding",
                    "message": "Building name set nahi is.",
                    "severity": "low"
                })

            # Check 2: Element counts validation
            element_counts = self.count_elements()

            if element_counts.get("walls", 0) == 0:
                validation_results["errors"].append({
                    "type": "No Walls Found",
                    "location": "IfcWall elements",
                    "message": "Building in koi bhi wall nahi is. Ye structural issue ho sakta is.",
                    "severity": "high"
                })
                validation_results["is_valid"] = False

            if element_counts.get("slabs", 0) == 0:
                validation_results["warnings"].append({
                    "type": "No Slabs Found",
                    "location": "IfcSlab elements",
                    "message": "Floor slabs nahi mile. Floors properly define nahi are.",
                    "severity": "medium"
                })

            if element_counts.get("doors", 0) == 0:
                validation_results["warnings"].append({
                    "type": "No Doors Found",
                    "location": "IfcDoor elements",
                    "message": "Building in darwaze nahi are. Entry/exit points missing are.",
                    "severity": "medium"
                })

            if element_counts.get("windows", 0) == 0:
                validation_results["warnings"].append({
                    "type": "No Windows Found",
                    "location": "IfcWindow elements",
                    "message": "Khidkiyan nahi are. Natural light aur ventilation for windows should be.",
                    "severity": "low"
                })

            # Check 3: Materials validation
            materials = self.get_materials()
            if not materials or materials == ["No materials found"]:
                validation_results["errors"].append({
                    "type": "No Materials Defined",
                    "location": "IfcMaterial",
                    "message": "Building materials define nahi are. Cost estimation aur analysis for materials zaruri are.",
                    "severity": "high"
                })
                validation_results["missing_elements"].append("Materials (IfcMaterial)")

            # Check 4: Spaces validation
            spaces = self.get_spaces()
            if not spaces or spaces[0].get("name") == "No spaces found":
                validation_results["warnings"].append({
                    "type": "No Spaces Defined",
                    "location": "IfcSpace",
                    "message": "Rooms/spaces define nahi are. Space planning incomplete is.",
                    "severity": "medium"
                })

            # Check 5: Structural elements
            if element_counts.get("columns", 0) == 0 and element_counts.get("beams", 0) == 0:
                validation_results["warnings"].append({
                    "type": "No Structural Elements",
                    "location": "IfcColumn, IfcBeam",
                    "message": "Columns aur beams nahi are. Structural framework incomplete lag raha is.",
                    "severity": "medium"
                })

            # Recommendations
            if len(validation_results["errors"]) > 0:
                validation_results["recommendations"].append(
                    "Critical errors are. Pehle inhe fix karo before construction."
                )

            if len(validation_results["warnings"]) > 3:
                validation_results["recommendations"].append(
                    "Bahut saari warnings are. IFC file the review karo aur missing elements add karo."
                )

            total_issues = len(validation_results["errors"]) + len(validation_results["warnings"])
            validation_results["total_issues"] = total_issues
            validation_results["error_count"] = len(validation_results["errors"])
            validation_results["warning_count"] = len(validation_results["warnings"])

            print(f"[OK] Validation complete: {total_issues} issues found")
            return validation_results

        except Exception as e:
            print(f"[ERROR] Error validating IFC file: {str(e)}")
            return {
                "is_valid": False,
                "errors": [{"type": "Validation Error", "message": str(e), "severity": "critical"}],
                "warnings": [],
                "missing_elements": [],
                "recommendations": [],
                "total_issues": 1,
                "error_count": 1,
                "warning_count": 0
            }

    def calculate_costing(self) -> Dict[str, Any]:
        """
        Building approximate costing calculate does
        Calculates approximate building costing

        Returns:
            Dict with cost breakdown and total cost
        """
        try:
            # Standard rates (approximate - INR per unit)
            rates = {
                "wall_per_sqm": 1500,  # Per square meter
                "door_per_unit": 8000,  # Per door
                "window_per_unit": 5000,  # Per window
                "slab_per_sqm": 2000,  # Per square meter
                "column_per_unit": 15000,  # Per column
                "beam_per_meter": 3000,  # Per meter
                "stair_per_unit": 50000,  # Per staircase
                "roof_per_sqm": 1800,  # Per square meter
            }

            element_counts = self.count_elements()

            # Calculate costs (simplified calculation)
            # Actual calculation would need area/length data from IFC
            costs = {
                "walls": element_counts.get("walls", 0) * rates["wall_per_sqm"] * 10,  # Assuming 10 sqm per wall avg
                "doors": element_counts.get("doors", 0) * rates["door_per_unit"],
                "windows": element_counts.get("windows", 0) * rates["window_per_unit"],
                "slabs": element_counts.get("slabs", 0) * rates["slab_per_sqm"] * 50,  # Assuming 50 sqm per slab
                "columns": element_counts.get("columns", 0) * rates["column_per_unit"],
                "beams": element_counts.get("beams", 0) * rates["beam_per_meter"] * 5,  # Assuming 5m per beam
                "stairs": element_counts.get("stairs", 0) * rates["stair_per_unit"],
                "roofs": element_counts.get("roofs", 0) * rates["roof_per_sqm"] * 100,  # Assuming 100 sqm per roof
            }

            # Material costs (if available)
            materials = self.get_materials()
            material_cost = 0
            if materials and materials != ["No materials found"]:
                material_cost = len(materials) * 50000  # Rough estimate

            costs["materials"] = material_cost

            # Calculate total
            total_construction_cost = sum(costs.values())

            # Add contingency and overhead (20%)
            contingency = total_construction_cost * 0.20
            total_cost = total_construction_cost + contingency

            costing_data = {
                "breakdown": costs,
                "subtotal": total_construction_cost,
                "contingency": contingency,
                "total_cost": total_cost,
                "currency": "INR",
                "note": "Ye approximate costing is. Actual cost area, quality, aur location par depend does.",
                "rates_used": rates
            }

            print(f"[OK] Cost calculated: INR {total_cost:,.2f}")
            return costing_data

        except Exception as e:
            print(f"[ERROR] Error calculating costing: {str(e)}")
            return {
                "breakdown": {},
                "subtotal": 0,
                "contingency": 0,
                "total_cost": 0,
                "currency": "INR",
                "note": f"Cost calculation in error: {str(e)}",
                "rates_used": {}
            }

    def extract_fast_summary(self) -> Dict[str, Any]:
        """
        Quick extraction - only essential data (FAST MODE)
        Sirf zaruri data extracts - bahut tez

        Returns:
            Essential building data (counts only, no validation/costing)
        """
        try:
            if not self.ifc_file:
                raise Exception("Pehle IFC file load karo / Load IFC file first")

            # Only basic info and counts - very fast
            fast_data = {
                "project_info": self.get_project_info(),
                "element_counts": self.count_elements(),
                "file_path": self.file_path,
                "mode": "fast_summary"
            }

            print("[OK] Fast summary extracted")
            return fast_data

        except Exception as e:
            print(f"[ERROR] Error extracting fast summary: {str(e)}")
            raise Exception(f"Fast data extraction failed: {str(e)}")

    def extract_full_data(self) -> Dict[str, Any]:
        """
        Saara building data ek saath extracts
        Extracts all building data together

        Returns:
            Complete building data dictionary
        """
        try:
            if not self.ifc_file:
                raise Exception("Pehle IFC file load karo / Load IFC file first")

            # Saara data collect karo / Collect all data
            full_data = {
                "project_info": self.get_project_info(),
                "element_counts": self.count_elements(),
                "materials": self.get_materials(),
                "spaces": self.get_spaces(),
                "validation": self.validate_ifc_file(),
                "costing": self.calculate_costing(),
                "file_path": self.file_path,
                "mode": "full_analysis"
            }

            print("[OK] Successfully extracted all building data")
            return full_data

        except Exception as e:
            print(f"[ERROR] Error extracting full data: {str(e)}")
            raise Exception(f"Data extraction failed: {str(e)}")


# Testing for / For testing
if __name__ == "__main__":
    parser = IFCParser()
    print("IFC Parser ready for use")
