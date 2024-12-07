import uuid
import json
import requests
import websocket
from typing import Callable

from awe.util.logging import logger
from awe.util.http import post_request
from awe.types.common import Payload, ResponseMessage
from awe.util.comfyui_exception import ComfyUIException
from awe.util.workflow import append_image_path, build_result, build_workflow, get_workflow_data, handle_image_result, handle_workflow_inputs

class ComfyUIClient:
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.current_task_id = None
    self.current_executed_node_ids = []
    self.current_total_node_ids = []
    self.current_progress = 0
    self.status = 'INIT'

  def connect(self):
    self.client_id = str(uuid.uuid4())
    self.ws = websocket.WebSocket()
    self.ws.connect(f"ws://{self.host}:{self.port}/ws?clientId={self.client_id}")
    
  def get_progress(self):
    if len(self.current_total_node_ids) == 0:
      progress = 1
    else:
      progress = int(len(self.current_executed_node_ids)*100/len(self.current_total_node_ids))

    # 如果 progress 为 0 ，设置其值为 1，与排队中任务的 progress 区分
    if progress == 0:
      progress = 1
    self.current_progress = progress
    return self.current_progress
  
  def queue_prompt(self, prompt: str):
    p = {"prompt": prompt, "client_id": self.client_id}
    response = post_request(f"{self.host}:{self.port}", '/prompt?client_id={self.client_id}', p)
    logger.info(f"[ComfyUIClient] Queue prompt response: {response}")
    return self.handle_response(response)
    
  def handle_response(self, response):
    status_code = response.status_code
    output = response.json()
    logger.info(f"[ComfyUIClient] Queue prompt response: status_code: {status_code}, output: {output}")
    if output is None:
      logger.info(f"[ComfyUIClient] Failed to queue prompt, output is None, status_code: {status_code}")
      return None
    error = output.get('error', {})
    node_errors = output.get('node_errors', {})
    if isinstance(node_errors, list):
      logger.info(f"[ComfyUIClient] Node errors is a list, node_errors: {node_errors}")
      node_errors = node_errors[0] if len(node_errors) > 0 else {}
    if len(error.keys()) > 0 or len(node_errors.keys()) > 0:
      logger.info(f"[ComfyUIClient] Failed to queue prompt, error: {error}, node_errors: {node_errors}")
      self.handle_error(output, error, node_errors)
      return None
    return output
  
  def check_status(self):
    if self.status in ['INIT', 'COMPLETED']:
      self.status = 'RUNNING'
    elif self.status == 'RUNNING':
      raise RuntimeError("ComfyUI workflow is already running, please wait for the previous workflow to complete")
    else:
      raise RuntimeError(f"ComfyUI workflow status is invalid: {self.status}")
  
  def init_status(self, payload: Payload):
    self.current_task_id = payload.taskId
    self.current_executed_node_ids = []
    self.current_progress = 0
    self.current_payload = payload
    
  def init_total_node_ids(self, workflow: dict):
    self.current_total_node_ids = list(workflow.keys()) if workflow else []
    
  def get_node_metadata(self, node_id: str):
    node = self.current_payload.workflow.get(node_id, {})
    meta = node.get("_meta", {})
    class_type = node.get("class_type", "Unknown Class Type")
    return {
      "title": meta.get("title", "Unknown Title"),
      "class_type": class_type
    }
  
  def run(self, payload: Payload):
    result = None
    try:
      # 0. 检查状态
      self.check_status()
      self.init_status(payload)
      # 1. 获取包含 paramTpl, outputTpl 和 contentTpl 的 workflow_data
      workflow_data = self.get_workflow(payload)
      # 2. 构建 workflow
      workflow = self.build_workflow(workflow_data)
      # 3. 初始化状态
      self.init_total_node_ids(workflow)
      # 4. 处理 workflow 的 inputs
      try:
        handle_workflow_inputs(workflow)
      except Exception as e:
        logger.error(f"[ComfyUIClient] Failed to handle workflow inputs, error: {e}")
        raise e
      # 3. 发送 workflow 到 ComfyUI
      response = self.queue_prompt(workflow)
      # 4. 获取结果
      if response is None:
        logger.info("[ComfyUIClient] Failed to queue prompt, response is None")
        return None
      prompt_id = response.get('prompt_id')
      self.wait_for_prompt_completion(prompt_id)
      comfyui_result = self.get_history(prompt_id)
      # 5. 构建结果
      result = self.build_result(comfyui_result, workflow_data)
      return result
    except Exception as e:
      logger.error(f"[ComfyUIClient] Failed to run workflow, error: {e}")
      if isinstance(e, ComfyUIException):
        self.handle_exception(e)
      else:
        raise e
    finally:
      self.status = 'COMPLETED'
      self.handle_complete_event(result)
      
  def get_workflow(self, payload: Payload):
    tag = payload.messageTag
    if tag == 'WEB' or tag == 'COMFYUI_API':
      return payload.workflow
    return get_workflow_data(payload)
    
  def build_workflow(self, workflow_data):
    tag = self.current_payload.messageTag
    # 如果 tag 是 WEB 或者 COMFYUI_API, 则直接返回 payload.prompt 或者 payload.workflow
    if tag == 'WEB' or tag == 'COMFYUI_API':
      return self.current_payload.prompt or self.current_payload.workflow
    # 否则, 调用 utils.build_workflow 方法
    params = self.current_payload.get('params')
    return build_workflow(workflow_data, params)

  def build_result(self, comfyui_result, workflow_data):
    tag = self.current_payload.messageTag
    logger.info(f"[ComfyUIClient] Building result, comfyui_result: {comfyui_result}")
    if tag == 'WEB':
      result = comfyui_result
    else: 
      handle_image_result(comfyui_result)
      result = build_result(comfyui_result, workflow_data)
    logger.info(f"[ComfyUIClient] Built result: {result}")
    return result

  def handle_exception(self, e: Exception):
    if isinstance(e, ComfyUIException):
      node_id = e.node_id
      node_type = e.node_type
    else:
      node_id = None
      node_type = None
    response_message = ResponseMessage({
      "type": 'ERROR',
      "code": "500",
      "client_id": self.current_payload.clientId,
      "task_id": self.current_payload.taskId,
      "response": { 
        'error': {
          'data': {
            'exception_message': f'{e}',
            'node_id': node_id,
            'node_type': node_type,
          }
        }
      }
    })
    self.handle_response_event(response_message)

  def handle_error(self, output: dict, error: dict, node_errors: dict):
    node_type = 'Unknown'
    error_msg = error.get('message', '')
    error_details = error.get('details', '')
    error_message = f'{error_msg}\n{error_details}'
    # node_errors 是一个dict，获取第一个错误节点
    if len(node_errors.keys()) > 0:
      node_id = list(node_errors.keys())[0]
      node_error = node_errors[node_id]
      node_type = node_error.get('class_type')
      error = node_error.get('errors', [])[0]
      error_message += f'\n{error.get("message", "")}\n{error.get("details", "")}'
    try:
      node_id = node_id or output.detail.split("#")[1].replace("'", "")
    except Exception as e:
      logger.info(f"[ComfyUIClient] Failed to get node_id from detail, error: {e}")
      node_id = 'Unknown'
      
    logger.info(f"send error msg: {node_id} {node_type} {error_message}")
    response_message = ResponseMessage({
      "type": 'ERROR',
      "code": "500",
      "client_id": self.current_payload.clientId,
      "task_id": self.current_payload.taskId,
      "response": {
        "error": {
          "data": {
            "node_id": node_id,
            "node_type": node_type,
            "exception_message": f"{error_message}",
          }
        }
      }
    })
    self.handle_response_event(response_message)

  def handle_progress_event(self, message):
    # 如果 message 是 progress 类型，则发送 debounced 为 True 的响应消息
    message_type = message.get("type")
    debounced = message_type == "progress"
    # 仅 WEB 类型需要处理图片
    if message_type == "executed" and self.current_payload.messageTag == 'WEB':
      message_data = message.get("data")
      if message_data is not None:
        output = message_data.get("output")
        if output is not None:
          for key in output:
            if key in ['images', 'gifs']:
              append_image_path(output[key])
    response = {
      "progressData": message,
      **message # FIXME 兼容旧版本
    }
    # 非 WEB 类型需要返回 progress
    if self.current_payload.messageTag != 'WEB':
      response["progress"] = self.get_progress()
    response_message = ResponseMessage({
      "type": 'PROGRESS',
      "code": "0",
      "debounced": debounced,
      "client_id": self.current_payload.clientId,
      "task_id": self.current_payload.taskId,
      "response": response
    })
    
    self.handle_response_event(response_message)

  def handle_complete_event(self, result):
    response = {
      "data": result
    }
    # WEB 类型需要返回 results
    if self.current_payload.messageTag == 'WEB':
      response["results"] = {}
      response["data"] = {}
    response_message = ResponseMessage({
      "type": 'COMPLETED',
      "code": "0",
      "client_id": self.current_payload.clientId,
      "task_id": self.current_payload.taskId,
      "response": response
    })
    self.handle_response_event(response_message)
  
  def get_history(self, prompt_id):
    response = requests.get(f"http://{self.host}:{self.port}/history/{prompt_id}")
    output = response.json()
    return output[prompt_id]["outputs"]

  def append_current_executed_node_list(self, node_id):
    # 如果 node_id 不在 current_executed_node_ids 中，则添加到 current_executed_node_ids 中
    if node_id not in self.current_executed_node_ids:
      self.current_executed_node_ids.append(node_id)
    
  def update_progress(self, data):
    # 更新 current_executed_node_ids
    self.append_current_executed_node_list(data["node"])
    # 更新 progress
    self.current_progress = self.get_progress()

  def wait_for_prompt_completion(self, prompt_id):
    if prompt_id is None:
      logger.info("[ComfyUIClient] Prompt ID is None, return")
      return
    while True:
      out = self.ws.recv()
      if not isinstance(out, str):
        logger.info(f"[ComfyUIClient] Received non-string message: {out}")
        continue
      
      message = json.loads(out)
      message_type = message.get("type")
      logger.info(f"[ComfyUIClient] Received message type: {message_type}")
      self.handle_progress_event(message)
      if message_type == "executing":
        data = message["data"]
        if data["prompt_id"] != prompt_id:
          logger.info(f"[ComfyUIClient] Received message for another prompt: {data['prompt_id']}")
          continue
        if data["node"] is None:
          # 如果 node 为空则表示任务执行完成
          self.current_executed_node_ids = self.current_total_node_ids
          break
        logger.info(f"[ComfyUIClient] Executing node {data['node']}")
        self.update_progress(data)
      else:
        logger.info(f"[ComfyUIClient] Received unexpected message type: {message_type}")

  def on_progress(self, callback: Callable):
    self.progress_callback = callback

  def on_error(self, callback: Callable):
    self.error_callback = callback

  def on_complete(self, callback: Callable):
    self.complete_callback = callback

  def handle_response_event(self, response_message: ResponseMessage):
    if response_message.type == 'PROGRESS':
      self.progress_callback(response_message, self.current_payload) if self.progress_callback else None
    elif response_message.type == 'ERROR':
      self.error_callback(response_message, self.current_payload) if self.error_callback else None
    elif response_message.type == 'COMPLETED':
      self.complete_callback(response_message, self.current_payload) if self.complete_callback else None
