from fastapi import APIRouter, Request, status
from typing import List, Optional
from models.workflow import Workflow, WorkflowUpdate, Action, ActionUpdate
from controllers.controller import *
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from fastapi import Depends

router = APIRouter(prefix="/workflow", tags=["workflows"])

@router.post("/create", response_description="create new workflow", status_code=status.HTTP_201_CREATED, response_model=Workflow)
def create(request: Request, workflow: Workflow, session: SessionContainer = Depends(verify_session())):
    return create_workflow(request, workflow, session)

@router.get("/get/{workflowid}", response_description="get workflow", status_code=status.HTTP_200_OK, response_model=Workflow)
def find_workflow(request: Request, workflowid: str, session: SessionContainer = Depends(verify_session())):
    return get_workflow(request, workflowid)

@router.get("/all", response_description="Get all workflows or workflows for a particular service", status_code=status.HTTP_200_OK, response_model=List[Workflow])
def find_workflows(request: Request, serviceName: Optional[str] = None, session: SessionContainer = Depends(verify_session())):
    return get_all_workflows(request, serviceName)
    
@router.put("/update/{workflowid}", response_description="update workflow", status_code=status.HTTP_200_OK, response_model=WorkflowUpdate)
def update(request: Request, workflowid: str, workflow: WorkflowUpdate, session: SessionContainer = Depends(verify_session())):
    return update_workflow(request, workflowid, workflow, session)

@router.delete("/delete/{workflowid}", response_description="delete workflow", status_code=status.HTTP_200_OK)
def delete(request: Request, workflowid: str, session: SessionContainer = Depends(verify_session())):
    delete_wf = delete_workflow(request, workflowid, session)
    return delete_wf

@router.post("/add/{workflowid}", response_description="add action to a workflow", status_code=status.HTTP_200_OK)
def add_action(request: Request, workflowid: str, action: Action, session: SessionContainer = Depends(verify_session())):
    return append_action(request, workflowid, action, session)

@router.put("/{workflowid}/updateaction/{actionid}", response_description="update action", status_code=status.HTTP_200_OK, response_model=ActionUpdate)
def update_act(request: Request, workflowid: str, actionid: str, action: Action, session: SessionContainer = Depends(verify_session())):
    return update_action(request, workflowid, actionid, action, session)