from models.workflow import Workflow, WorkflowUpdate, Action, ActionUpdate
from fastapi import Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from supertokens_python.recipe.session import SessionContainer
from typing import Optional


def get_collection(request: Request) :
    return request.app.database["workflows"]

def get_user_collection(request: Request) :
    return request.app.database["users"]

def create_workflow(request: Request, workflow: Workflow, session: SessionContainer):
    user_id = session.get_user_id()
    user_role = get_user_collection(request).find_one({"userId": user_id})["role"]
    if(user_role != "admin") :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Only admins can access this route")
    workflow = jsonable_encoder(workflow)
    new_workflow = get_collection(request).insert_one(workflow)
    created_workflow = get_collection(request).find_one({"_id": new_workflow.inserted_id})
    return created_workflow

def get_workflow(request: Request, workflow_id: str) :
    workflow = get_collection(request).find_one({"_id": workflow_id})
    if not workflow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Workflow with name {workflow_id} not found")
    return workflow

def get_all_workflows(request: Request, serviceName: Optional[str] = None):
    if serviceName:
        workflows = list(get_collection(request).find({"workFlowServiceName": serviceName}))
    else:
        workflows = list(get_collection(request).find({}))
    return workflows

def update_workflow(request: Request, workFlowId: str, workFlow: WorkflowUpdate, session: SessionContainer) :
    user_id = session.get_user_id()
    user_role = get_user_collection(request).find_one({"userId": user_id})["role"]
    if(user_role != "admin") :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Only admins can access this route")
    workFlow = jsonable_encoder(workFlow)
    update_result = get_collection(request).update_one(
        {"_id": workFlowId}, {"$set": workFlow}
    )
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Workflow not found")
    else :
        updated_workflow = get_collection(request).find_one({"_id": workFlowId})
        return updated_workflow

def delete_workflow(request: Request, workFlowId: str, session: SessionContainer):
    user_id = session.get_user_id()
    user_role = get_user_collection(request).find_one({"userId": user_id})["role"]
    if(user_role != "admin") :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Only admins can access this route")
    delete_result = get_collection(request).delete_one({"_id": workFlowId})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return {"message": "Workflow deleted successfully"}

def append_action(request: Request, workflow_id: str, action: Action, session: SessionContainer):
    user_id = session.get_user_id()
    user_role = get_user_collection(request).find_one({"userId": user_id})["role"]
    if(user_role != "admin") :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Only admins can access this route")
    action = jsonable_encoder(action)
    update_result =  get_collection(request).update_one(
        {"_id": workflow_id}, {"$push": {"actionsToPerform": action}}
    )
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Workflow not found")
    updated_workflow = get_collection(request).find_one({"_id": workflow_id})
    return updated_workflow

def update_action(request: Request, workflow_id: str, action_id: str, action_update: ActionUpdate, session: SessionContainer):
    user_id = session.get_user_id()
    user_role = get_user_collection(request).find_one({"userId": user_id})["role"]
    if(user_role != "admin") :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Only admins can access this route")
    workflow = get_collection(request).find_one({"_id": workflow_id})
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    actions = workflow.get("actionsToPerform", [])
    action_index = next((index for (index, action) in enumerate(actions) if action["_id"] == action_id), None)
    
    if action_index is None:
        raise HTTPException(status_code=404, detail="Action not found")
    
    updated_action_data = {**actions[action_index], **action_update.dict(exclude_unset=True)}
    actions[action_index] = updated_action_data

    update_result = get_collection(request).update_one(
        {"_workFlowId": workflow_id},
        {"$set": {"actionsToPerform": actions}}
    )
    
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Failed to update action")

    updated_workflow = get_collection(request).find_one({"_workFlowId": workflow_id})
    return updated_workflow