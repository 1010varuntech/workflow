import uuid
from typing import Optional, Union, List
from pydantic import BaseModel, Field
from enum import Enum
from datetime import date

class ActionType(str, Enum):
    user = "user"
    aiAction = "aiAction"

class ActionTypeEnum(str, Enum):
    scroll = "scroll"
    click = "click"
    submit = "submit"
    type = "type"
    fill = "fill"
    clickOver = "clickOver"

class ActionDetail(BaseModel):
    type: ActionTypeEnum
    value: Union[str, int, float, None] = None

class Action(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    actionTitle: str
    description: str
    toolUrl: str
    action: ActionDetail
    elemPath: str
    eleClass: str
    eleId: str
    actionType: ActionType

    class Config:
        json_schema_extra = {
            "example": {
                "_id": "123654789",
                "actionTitle": "Locate button",
                "description": "this action is used to locate the button",
                "toolUrl": "http://example.com",
                "action": {
                    "type": "click",
                    "value": None
                },
                "elamPath": "sample path",
                "elemClass": "div",
                "elemId": "button",
                "actionType": "user"
            }
        }

class ActionUpdate(BaseModel):
    actionTitle: Optional[str] = None
    description: Optional[str] = None
    toolUrl: Optional[str] = None
    action: Optional[ActionDetail] = None
    elemPath: Optional[str] = None
    eleClass: Optional[str] = None
    eleId: Optional[str] = None
    actionType: Optional[ActionType] = None

    class Config:
        json_schema_extra = {
            "example": {
                "_id": "123654789",
                "actionTitle": "Locate button",
                "description": "this action is used to locate the button",
                "toolUrl": "http://example.com",
                "action": {
                    "type": "click",
                    "value": None
                },
                "elamPath": "sample path",
                "elemClass": "div",
                "elemId": "button",
                "actionType": "user"
            }
        }

class Workflow(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    workFlowName: str
    endGoal: str
    variables: Optional[List[str]] = None
    workFlowServiceName: str
    createdAt: date =  date.today()
    updatedAt: date = date.today()
    actionsToPerform: List[Action]

    class Config:
        json_schema_extra = {
            "example": {
                "_id": "789654123",
                "workFlowName": "Login Workflow",
                "workFlowServiceName": "Linkedin",
                "variables": None,
                "endGoal": "user will be logged in",
                "actionsToPerform": [{
                "_id": "123654789",
                "actionTitle": "Locate button",
                "description": "this action is used to locate the button",
                "toolUrl": "http://example.com",
                "action": {
                    "type": "click",
                    "value": None
                },
                "elamPath": "sample path",
                "elemClass": "div",
                "elemId": "button",
                "actionType": "user"
            }],
            }
        }

class WorkflowUpdate(BaseModel):
    workFlowName: Optional[str] = None
    workFlowServiceName: str
    endGoal: Optional[str] = None
    variables: Optional[List[str]] = None
    updatedAt: date = date.today()
    actionsToPerform: Optional[List[Action]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "workFlowName": "Login Workflow",
                "variables": [""],
                "workFlowServiceName": "linkedin",
                "endGoal": "user will be logged in",
                "actionsToPerform": [],
            }
        }