from fastapi import APIRouter, Request, status
from typing import List
from models.workflow import Workflow, WorkflowUpdate, Action
from controllers.controller import *
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from fastapi import Depends

router = APIRouter(prefix="/workflow", tags=["workflows"])

@router.post("/create", response_description="create new workflow", status_code=status.HTTP_201_CREATED, response_model=Workflow)
def create(request: Request, workflow: Workflow, session: SessionContainer = Depends(verify_session())):
    return create_workflow(request, workflow, session)

@router.get("/get/{workflowname}", response_description="get workflow", status_code=status.HTTP_200_OK, response_model=Workflow)
def find_workflow(request: Request, workflowname: str, session: SessionContainer = Depends(verify_session())):
    return get_workflow(request, workflowname)

@router.get("/all/{serviceName}", response_description="get all workflows", status_code=status.HTTP_200_OK, response_model=List[Workflow])
def find_workflows(request: Request, serviceName: str, session: SessionContainer = Depends(verify_session())):
    return get_all_workflows(request, serviceName)
    
@router.put("/update/{workflowname}", response_description="update workflow", status_code=status.HTTP_200_OK, response_model=WorkflowUpdate)
def update(request: Request, workflowname: str, workflow: WorkflowUpdate, session: SessionContainer = Depends(verify_session())):
    return update_workflow(request, workflowname, workflow, session)

@router.delete("/delete/{workflowid}", response_description="delete workflow", status_code=status.HTTP_200_OK)
def delete(request: Request, workflowid: str, session: SessionContainer = Depends(verify_session())):
    delete_wf = delete_workflow(request, workflowid, session)
    return delete_wf

@router.post("/add/{workflowid}", response_description="add action to a workflow", status_code=status.HTTP_200_OK)
def update_action(request: Request, workflowid: str, action: Action, session: SessionContainer = Depends(verify_session())):
    return append_action(request, workflowid, action, session)