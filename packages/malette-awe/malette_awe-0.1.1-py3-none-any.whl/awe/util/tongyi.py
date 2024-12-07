# -*- coding: utf-8 -*-
from http import HTTPStatus
import random
import sys
import os
import dashscope
from awe.util.logging import logger

api_key = os.getenv('DASHSCOPE_API_KEY')

def translate(text):
  response = dashscope.Generation.call(
    model='qwen-max',
    seed=random.randint(0, sys.maxsize),
    top_p=0.8,
    result_format='message',
    enable_search=False,
    max_tokens=1500,
    temperature=0.85,
    repetition_penalty=1.0,
    prompt=f"帮我把这段绘画描述转换成 Stable Diffusion 绘画所需的英文提示词：{text}，请直接给我结果，不要给我提示，不要给我提示，不要给我额外描述，方便我通过程序进行解析",
    api_key=api_key
  )
  if response.status_code == HTTPStatus.OK:
    # 安全地获取content字段的值
    content = None
    if "output" in response and "choices" in response["output"] and response["output"]["choices"]:
      first_choice = response["output"]["choices"][0]
      if "message" in first_choice and "content" in first_choice["message"]:
        content = first_choice["message"]["content"]

    if content is not None:
      logger.info('返回内容: %s', content)
    else:
      logger.info("Content not found or the JSON structure was unexpected.")
    return content or text
  else:
    logger.info('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
        response.request_id, response.status_code,
        response.code, response.message
    ))