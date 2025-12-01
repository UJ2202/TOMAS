from fastapi import APIRouter, HTTPException
from typing import List

from core.mode_registry import registry
from core.mode import AgentMode

router = APIRouter(tags=["modes"])

@router.get("/modes")
def list_modes():
    """List all available agent modes"""
    modes = registry.list_all()
    return {
        "modes": [
            {
                "id": m.id,
                "name": m.name,
                "description": m.description,
                "category": m.category,
                "icon": m.icon,
                "endpoint_path": m.endpoint_path
            }
            for m in modes
        ],
        "count": len(modes)
    }

@router.get("/modes/{mode_id}")
def get_mode_details(mode_id: str):
    """Get detailed configuration for a specific mode"""
    mode = registry.get(mode_id)
    if not mode:
        raise HTTPException(status_code=404, detail=f"Mode '{mode_id}' not found")

    return {
        "id": mode.id,
        "name": mode.name,
        "description": mode.description,
        "category": mode.category,
        "icon": mode.icon,
        "inputs": [field.dict() for field in mode.inputs],
        "outputs": [output.dict() for output in mode.outputs],
        "endpoint_path": mode.endpoint_path
    }
