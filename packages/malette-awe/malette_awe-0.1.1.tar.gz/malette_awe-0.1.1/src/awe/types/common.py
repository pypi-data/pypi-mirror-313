import json
from pydantic import BaseModel, Field

class Payload(BaseModel):
  """Payload

  Args:
    api
    taskId
    userId
    workflowCode
    params
    workflow
    workflowUrl

  Returns:
      _type_: _description_
  """
  api: str = Field(title="api", description="api", default=None)
  taskId: str = Field(title="taskId", description="taskId", default=None)
  clientId: str = Field(title="clientId", description="clientId", default=None)
  userId: str = Field(title="userId", description="userId", default=None)
  workflowCode: str = Field(title="workflowCode", description="workflowCode", default=None)
  params: dict = Field(title="params", description="params", default=None)
  workflow: dict = Field(title="workflow", description="workflow", default=None)
  workflowUrl: str = Field(title="workflowUrl", description="workflowUrl", default=None)
  engine: str = Field(title="engine", description="engine", default="ComfyUI")
  prompt: dict = Field(title="prompt", description="prompt", default=None)
  messageTag: str = Field(title="messageTag", description="messageTag", default=None)
  
  def get(self, key):
    return getattr(self, key)
  
  # 静态方法 parse_raw
  @staticmethod
  def parse_raw(payload: str):
    return Payload(**json.loads(payload))

class CommonResponse(BaseModel):
    success: bool = Field(title="success", description="success", default=True)
    code: str = Field(title="code", description="code", default="0")
    message: str = Field(title="message", description="message", default="")
    data: dict = Field(title="data", description="data", default=None)
    
class ResponseMessage:
  def __init__(self, params):
    self.type = params.get('type')
    self.payload: Payload = params.get('payload')
    self.response: CommonResponse = params.get('response')
    self.tag = params.get('tag')
    self.code = params.get('code')
    self.message = params.get('message')
    self.client_id = params.get('client_id')
    self.task_id = params.get('task_id')
    self.debounced = params.get('debounced')
    self.progress = params.get('progress')
    self.workflow_code = params.get('workflow_code')
    self.app_name = params.get('app_name')
    self.debounced = params.get('debounced')

  def get(self, key):
    return getattr(self, key)