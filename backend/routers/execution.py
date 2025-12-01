from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Request, BackgroundTasks
from typing import List, Optional
import json
from pathlib import Path

from core.mode_registry import registry

router = APIRouter(tags=["execution"])

# In-memory task storage (use Redis in production)
tasks = {}

@router.post("/execute")
async def execute_mode(
    request: Request,
    background_tasks: BackgroundTasks,
    mode_id: str = Form(...),
    input_data: str = Form(...),
    files: Optional[List[UploadFile]] = File(None)
):
    """
    Execute an agent mode

    Returns immediately with task_id
    Execution happens in background
    """
    # Get services from app state
    denario_service = request.app.state.denario_service
    mode_executor = request.app.state.mode_executor

    # Get mode
    mode = registry.get(mode_id)
    if not mode:
        raise HTTPException(status_code=404, detail=f"Mode '{mode_id}' not found")

    # Parse input data
    try:
        input_dict = json.loads(input_data)
    except:
        raise HTTPException(status_code=400, detail="Invalid input_data JSON")

    # Create session
    session_id = denario_service.create_session()

    # Save uploaded files
    if files:
        session_dir = denario_service.get_session_dir(session_id)
        input_dir = session_dir / "input_files"
        input_dir.mkdir(exist_ok=True)

        uploaded_filenames = []
        for file in files:
            file_path = input_dir / file.filename
            with open(file_path, 'wb') as f:
                content = await file.read()
                f.write(content)
            uploaded_filenames.append(file.filename)

        input_dict['uploaded_files'] = uploaded_filenames

    # Create task
    task_id = session_id  # Use session_id as task_id
    tasks[task_id] = {
        "id": task_id,
        "mode_id": mode_id,
        "status": "queued",
        "progress": 0,
        "result": None,
        "error": None
    }

    # Execute in background
    background_tasks.add_task(
        _execute_task,
        task_id,
        mode,
        mode_executor,
        session_id,
        input_dict
    )

    return {
        "task_id": task_id,
        "session_id": session_id,
        "status": "queued"
    }

async def _execute_task(task_id, mode, mode_executor, session_id, input_data):
    """Background task execution"""
    try:
        tasks[task_id]["status"] = "executing"
        tasks[task_id]["progress"] = 10

        # Execute mode
        result = await mode_executor.execute(mode, session_id, input_data)

        tasks[task_id]["status"] = "completed"
        tasks[task_id]["progress"] = 100
        tasks[task_id]["result"] = result

    except Exception as e:
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["error"] = str(e)
        print(f"❌ Task {task_id} failed: {str(e)}")

@router.get("/tasks/{task_id}/status")
def get_task_status(task_id: str):
    """Get task status"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    task = tasks[task_id]
    return {
        "task_id": task["id"],
        "status": task["status"],
        "progress": task["progress"],
        "error": task["error"]
    }

@router.get("/tasks/{task_id}/results")
def get_task_results(task_id: str):
    """Get task results"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    task = tasks[task_id]
    if task["status"] != "completed":
        raise HTTPException(status_code=400, detail="Task not completed")

    return {
        "task_id": task["id"],
        "result": task["result"]
    }
