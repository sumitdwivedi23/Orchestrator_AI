from langchain_core.tools import tool

@tool
def validate_design_spec(spec: str) -> dict:
    """Validates the architectural design specification."""
    try:
        
        if not spec or len(spec.split()) < 10:
            return {"valid": False, "error": "Design specification too short or empty"}
        return {"valid": True, "error": None}
    except Exception as e:
        return {"valid": False, "error": str(e)}

@tool
def calculate_resource_requirements(spec: str) -> dict:
    """Calculates resource requirements based on design spec."""
    try:
        
        words = len(spec.split())
        return {
            "compute_units": words // 10,
            "memory_gb": words // 20,
            "storage_tb": words // 50
        }
    except Exception as e:
        return {"error": str(e)}