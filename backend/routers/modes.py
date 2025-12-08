"""
Modes Router

API endpoints for listing and retrieving mode information.
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

from core.mode_registry import ModeRegistry


router = APIRouter(tags=["modes"])


@router.get("/modes")
def list_modes():
    """
    List all available agent modes

    Returns:
        Dictionary with list of modes and count
    """
    modes = ModeRegistry.list_modes()

    return {
        "modes": [
            {
                "id": mode.id,
                "name": mode.name,
                "description": mode.description,
                "category": mode.category,
                "icon": mode.icon,
                "engine": mode.engine.value,
                "tags": mode.tags,
                "estimated_time": mode.estimated_time,
                "cost_estimate": mode.cost_estimate
            }
            for mode in modes
        ],
        "count": len(modes)
    }


@router.get("/modes/{mode_id}")
def get_mode_details(mode_id: str):
    """
    Get detailed configuration for a specific mode

    Args:
        mode_id: Mode identifier

    Returns:
        Detailed mode configuration

    Raises:
        HTTPException: If mode not found
    """
    mode = ModeRegistry.get_mode(mode_id)
    if not mode:
        raise HTTPException(
            status_code=404,
            detail=f"Mode '{mode_id}' not found"
        )

    return {
        "id": mode.id,
        "name": mode.name,
        "description": mode.description,
        "category": mode.category,
        "icon": mode.icon,
        "engine": mode.engine.value,
        "inputs": [field.model_dump() for field in mode.inputs],
        "outputs": [output.model_dump() for output in mode.outputs],
        "config": mode.config.model_dump() if mode.config else {},
        "tags": mode.tags,
        "estimated_time": mode.estimated_time,
        "cost_estimate": mode.cost_estimate,
        "examples": mode.examples,
        "tips": mode.tips
    }


@router.get("/modes/category/{category}")
def list_modes_by_category(category: str):
    """
    List modes filtered by category

    Args:
        category: Category to filter by

    Returns:
        Dictionary with filtered modes
    """
    all_modes = ModeRegistry.list_modes()
    filtered_modes = [mode for mode in all_modes if mode.category == category]

    return {
        "category": category,
        "modes": [
            {
                "id": mode.id,
                "name": mode.name,
                "description": mode.description,
                "icon": mode.icon,
                "engine": mode.engine.value
            }
            for mode in filtered_modes
        ],
        "count": len(filtered_modes)
    }


@router.get("/modes/engine/{engine_type}")
def list_modes_by_engine(engine_type: str):
    """
    List modes filtered by engine type

    Args:
        engine_type: Engine type to filter by (cmbagent, denario, etc.)

    Returns:
        Dictionary with filtered modes
    """
    all_modes = ModeRegistry.list_modes()
    filtered_modes = [mode for mode in all_modes if mode.engine.value == engine_type]

    return {
        "engine": engine_type,
        "modes": [
            {
                "id": mode.id,
                "name": mode.name,
                "description": mode.description,
                "icon": mode.icon,
                "category": mode.category
            }
            for mode in filtered_modes
        ],
        "count": len(filtered_modes)
    }
