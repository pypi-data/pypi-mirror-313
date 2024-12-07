import os
import re
import sys
import random
import base64
import traceback
from io import BytesIO

from src.oss import get_download_url, get_file_content, upload_file
from src.types.common import Payload
from src.util.util import generate_filename_with_date, get_file_extension, get_remote_base64_image, get_remote_json, upload_image_to_comfyui, upload_remote_image
from src.util.logging import logger
from src.util.tongyi import translate as tongyi_translate
from src.util.comfyui_exception import ComfyUIException

def contains_chinese(check_str):
  return re.search('[\u4e00-\u9fff]', check_str)

def translate(text):
  logger.info(f"translate text: {text}")
  if contains_chinese(text):
    logger.info(f"contains chinese, use tongyi translate: {text}")
    return tongyi_translate(text)
  else:
    logger.info(f"not contains chinese, use origin text: {text}")
  return text

def get_remote_workflow_from_oss(workflow_code):
  env = os.getenv('ENV')
  appname = os.getenv('APPNAME')
  file_path = f"ai-workflow-engine/workflows/{env}/{appname}/{workflow_code}.json"
  return get_file_content(file_path)

def get_workflow_data(payload: Payload):
  task_id = payload.get('taskId')
  # 这里的 workflow 并非 ComfyUI 的 workflow，而是包含 paramTpl, outputTpl 和 contentTpl 的 workflow
  workflow_data = payload.get('workflow')
  # 如果 workflow_data 为空，尝试从 workflowUrl 获取
  if workflow_data is None:
    workflow_url = payload.get('workflowUrl')
    # 如果 workflow_url 不为空，尝试从远程获取
    if workflow_url is not None:
      workflow_data = get_remote_json(workflow_url)
    # 如果从 workflowUrl 获取失败，尝试从 workflowCode 获取
    if workflow_data is None:
      workflow_code = payload.get('workflowCode')
      if workflow_code is not None:
        workflow_data = get_remote_workflow_from_oss(workflow_code)
  # 如果 workflow_data 为空，返回错误
  if workflow_data is None:
    logger.error(f"get workflow data failed, task_id: {task_id}")
    return None
  logger.info(f"workflow_data: {workflow_data}")
  return workflow_data

def build_workflow(workflow_data, params=None):
  if params is None:
    params = workflow_data.get('params')
  
  logger.info(f"workflow_data: {workflow_data}")
  logger.info(f"params: {params}")
  
  content_tpl = workflow_data.get('contentTpl')
  param_tpl = workflow_data.get('paramTpl')
  params = params or workflow_data.get('params')
  logger.info(f"workflow params: {params}")
  if params is None:
    logger.error("workflow params is None, just return content_tpl")
    return content_tpl
  if param_tpl is None:
    logger.error("workflow paramTpl is None, just return content_tpl")
    return content_tpl
  
  for key in param_tpl:
    param_node = param_tpl.get(f'{key}')
    node_id = param_node.get("nodeId")
    param_key = param_node.get("paramKey")
    param_type = param_node.get("paramType")
    param = params.get(f'{key}')
    node = content_tpl.get(f'{node_id}')
    if node is None:
      logger.error(f"node {node_id} is None, skip it.")
      continue
    inputs = node.get("inputs")
    if param_type is not None and param_type.upper() == "RANDOM":
      if inputs[f'{param_key}'] is None:
        inputs[f'{param_key}'] = random.randint(0, sys.maxsize)
      continue
      
    if param is None:
      logger.warning(f"param {key} is None")
      continue
    node = build_workflow_node(key, param_node, params, node, node_id)
    content_tpl[f'{node_id}'] = node
  
  return content_tpl

def build_workflow_node(key, param_node, params, node, node_id):
  inputs = node.get("inputs")
  param = params.get(f'{key}')
  param_key, param_type, enable_translate = (param_node.get("paramKey"), 
    param_node.get("paramType"), param_node.get("enableTranslate"))
  if param_type is None:
    logger.error(f"[WorkflowUtil] paramType is None, skip it, node_id: {node_id}, key: {key}")
    return node
  logger.info(f"[WorkflowUtil] param_type: {param_type}")
  if param_type.upper() == "STRING" or param_type.upper() == "TEXT":
    if enable_translate == 'Y':
      inputs[f'{param_key}'] = translate(param)
    else:
      inputs[f'{param_key}'] = param
  elif param_type.upper() == "IMAGE":
    build_image_node(param, inputs, node, node_id)
  elif param_type.upper() in ["INT", "FLOAT", "NUMBER"]:
    inputs[f'{param_key}'] = param
  elif param_type.upper() == "ARRAY":
    build_array_node(key, param_key, param_node, param, inputs)
  else:
    logger.warning(f"[WorkflowUtil] paramType not support: {param_type}")

  node["inputs"] = inputs
  return node

def build_image_node(param, inputs, node, node_id):
  handled = node.get('handled')
  if handled:
    logger.info(f"[WorkflowUtil] node {node_id} has been handled")
    return
  host = os.getenv('COMFYUI_HOST')
  port = os.getenv('COMFYUI_PORT')
  img_url = param
  class_type = node['class_type']
  if class_type == 'Base64ImageInput':
    inputs['base64_image'] = get_remote_base64_image(img_url)
  else:
    logger.info(f"[WorkflowUtil] image url: {img_url}")
    if img_url is None or type(img_url) is not str:
      logger.error(f"image is not url, node_id: {node_id}, type: {node['class_type']}")
      return
    elif img_url.startswith("http"):
      new_image_url = img_url
    else:
      new_image_url = get_download_url(img_url)
      logger.info(f"new_image_url : {new_image_url}")
    upload_url = f'http://{host}:{port}/upload/image'
    resp = upload_image_to_comfyui(upload_url, 'image.png', new_image_url)
    if resp is not None:
      inputs['image'] = resp.get('name')
      node['handled'] = True
  
def build_array_node(key, param_key, param_node, param, inputs):
  param_sub_type = param_node.get("paramSubType")
  if type(param) is not list:
    if (param_sub_type is None and type(param) is str):
      inputs[f'{param_key}'] = param
      return
    logger.error(f"param {key} is not list, but paramSubType is Array, skip it.")
    return
  if param_sub_type == "Image":
    inputs[f'{param_key}'] = [get_remote_base64_image(p) for p in param]
  else:
    inputs[f'{param_key}'] = param
         
def limit_input_value(input_key, inputs, max_value, options=None):
  if options is None:
    options = {}
  node = options.get('node')
  node_id = options.get('node_id')
  
  if isinstance(inputs[input_key], str):
    inputs[input_key] = int(inputs[input_key])
  
  if isinstance(inputs[input_key], (int, float)):
    if inputs[input_key] > max_value:
      inputs[input_key] = max_value
      logger.warning(f"Limiting {input_key} to {max_value}, {inputs}")
      raise ComfyUIException(f"{input_key} 不能大于 {max_value}", node_id, node.get('class_type', 'Unknown'))
 
def _handle_image_input(inputs, new_inputs, node, node_id):
  try:
    build_image_node(inputs['image'], new_inputs, node, node_id)
  except Exception as e:
    logger.error(f"[WorkflowUtil] handle image failed: {e}")
    raise ComfyUIException("图片有误，请重新上传", node_id, node.get('class_type', 'Unknown'))

def _process_input_key(key, inputs, new_inputs, node, node_id):
  if key == "image":
    _handle_image_input(inputs, new_inputs, node, node_id)
  elif key in ["seed", "noise_seed", "rand_seed"]:
    control_after_generate = inputs.get('control_after_generate') or 'randomize'
    if control_after_generate == 'fixed':
      new_inputs[key] = inputs[key]
    else:
      new_inputs[key] = random.randint(0, sys.maxsize)
  elif key == 'steps':
    limit_input_value(key, new_inputs, 40, {'node_id': node_id, 'node': node})
  elif key in ['scale', 'scale_by', 'upscale_by']:
    limit_input_value(key, new_inputs, 2, {'node_id': node_id, 'node': node})
  elif key in ['batch_size', 'amount', 'num_samples', 'num_samples_per_class', 'num_classes', 'num_classes_per_batch', 'num_classes_per_sample']:
    limit_input_value(key, new_inputs, 4, {'node_id': node_id, 'node': node})
  elif key in ['height', 'empty_latent_height', 'width', 'empty_latent_width', 'side_length', 'image_gen_width', 'image_gen_height']:
    limit_input_value(key, new_inputs, 2048, {'node_id': node_id, 'node': node})
  else:
    logger.warning(f"key {key} not support")

def handle_workflow_inputs(workflow):
  for node_id, node in workflow.items():
    try:
      inputs = node.get("inputs", {})
      new_inputs = {**inputs}
      
      for key in inputs:
        _process_input_key(key, inputs, new_inputs, node, node_id)
      
      node["inputs"] = new_inputs
      workflow[node_id] = node
        
    except Exception as e:
      logger.error(f"[WorkflowUtil] handle_workflow_inputs failed: {e}")
      logger.error(f"[WorkflowUtil] handle_workflow_inputs failed: {traceback.print_exc()}")
      if isinstance(e, ComfyUIException):
        raise e
      raise ComfyUIException(f"handle_workflow_inputs failed: {e}", node_id, node.get('class_type', 'Unknown'))
  
  return workflow
  
def build_remote_image_url():
  host = os.getenv('COMFYUI_HOST')
  port = os.getenv('COMFYUI_PORT')
  return f"http://{host}:{port}/view"
      
def _handle_dict_item(item, file_extension):
  if item.get("filename"):
    return _handle_filename_item(item, file_extension)
  elif item.get("id"):
    return _handle_id_item(item)
  else:
    logger.error(f"filename not found in item: {item}")
  return item

def _handle_filename_item(item, file_extension):
  if item.get('url') is not None and item.get('url').startswith("http"):
    logger.info(f"item url is {item.get('url')}, return it")
    return item
  path = generate_filename_with_date(get_file_extension(item["filename"]))
  preview_url = build_remote_image_url()
  new_path, file_url = upload_remote_image(preview_url, item, path, file_extension)
  return {**item, "url": file_url, "path": new_path}

def _handle_id_item(item):
    result = {**item}
    urls = {
      "image_url": "png",
      "video_url": "mp4",
      "audio_url": "mp3"
    }
    
    for url_key, ext in urls.items():
      url = item.get(url_key)
      if url:
        path = generate_filename_with_date(ext)
        new_url, _ = upload_remote_image(url, item, path, ext)
        result[url_key] = new_url
        if url_key == "image_url":
          result["path"] = new_url
    
    return result

def _handle_str_item(base64_image):
  if base64_image.startswith("http"):
    return {"url": base64_image, "path": base64_image}
  
  if base64_image.startswith("data:image"):
    path = generate_filename_with_date("png")
    image_bytes = base64.b64decode(base64_image)
    input_stream = BytesIO(image_bytes)
    file_url = upload_file(input_stream, path)
    return {"url": file_url, "path": path}
  
  logger.error(f"base64_image {base64_image} not support")
  return base64_image

def append_image_path(items, file_extension="png"):
  for i in range(len(items)):
    if isinstance(items[i], dict):
      items[i] = _handle_dict_item(items[i], file_extension)
    elif isinstance(items[i], str):
      items[i] = _handle_str_item(items[i])
    else:
      logger.error(f"item {items[i]} not support")

def handle_image_result(comfyui_result):
  try:
    for node_id in comfyui_result:
      node = comfyui_result.get(node_id)
      print(f"node: {node}")
      for key in node:
        item = node.get(key)
        if type(item) is dict:
          item = [item]
          append_image_path(item)
          node[key] = item[0]
        elif type(item) is list:
          append_image_path(item)
        else:
          logger.error(f"item {item} not support")
  except Exception as e:
    logger.error(f"[WorkflowUtil] handle_image_result failed: {e}")
    logger.error(f"[WorkflowUtil] handle_image_result failed: {traceback.print_exc()}")

def format_workflow_resp(resp, output_tpl):
  # 暂时只处理输出节点中的images
  result_obj = {}
  for key in output_tpl:
    output_config = output_tpl.get(key)
    node_id = output_config.get("nodeId")
    param_key = output_config.get("paramKey")
    node = resp.get("results").get(f'{node_id}')
    result = None
    try:
      result = node.get(param_key)
    except Exception as e:
      logger.error(f"get result failed: {e}")
    try:
      if key == "images" or output_config.get("paramType") == "Image":
        if result is None and param_key != "gifs":
          result = node.get("gifs")
    except Exception as e:
      logger.error(f"get result failed: {e}")
    result_obj[key] = {
      "output": result,
      "title": output_config.get("name"),
      "paramType": output_config.get("paramType"),
    }
  return result_obj

def build_result(comfyui_result, workflow_data):
  # 根据 output_tpl 格式化结果
  output_tpl = workflow_data.get('outputTpl')
  result = format_workflow_resp(comfyui_result, output_tpl)
  return result
