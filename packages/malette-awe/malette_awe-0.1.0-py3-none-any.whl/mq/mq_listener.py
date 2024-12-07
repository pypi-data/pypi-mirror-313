
import os
import traceback
from time import sleep
from typing import Callable
from threading import Thread
from pydantic import BaseModel, Field
from mq_http_sdk.mq_client import MQClient

from src.util.logging import logger
from src.types.common import Payload
from src.util.util import safe_json_loads

class MQListenerOptions(BaseModel):
  instance_id: str = Field(title="实例ID", description="实例ID", default="")
  request_topic: str = Field(title="MQ Topic", description="MQ Topic", default="")
  group_id: str = Field(title="MQ Group ID", description="MQ Group ID", default="")
  message_tag: str = Field(title="MQ Message Tag", description="MQ Message Tag", default="")
  batch: int = Field(title="批量消费消息数", description="批量消费消息数", default=1)
  wait_seconds: int = Field(title="等待时间", description="等待时间", default=3)
  callback: Callable = Field(title="回调函数", description="回调函数", default=None)
  env: str = Field(title="环境", description="环境", default="")
  appname: str = Field(title="应用名", description="应用名", default="")
  is_static_topic: bool = Field(title="是否为静态Topic", description="是否为静态Topic", default=False)
  is_static_group: bool = Field(title="是否为静态Group", description="是否为静态Group", default=False)
  endpoint: str = Field(title="MQ Endpoint", description="MQ Endpoint", default="")
  access_key: str = Field(title="MQ Access Key", description="MQ Access Key", default="")
  access_secret: str = Field(title="MQ Access Secret", description="MQ Access Secret", default="")

class MQListenerThread(Thread):
  def __init__(self, options: MQListenerOptions):
    super().__init__()
    self.mq_client = MQClient(
      options.endpoint,
      options.access_key,
      options.access_secret
    )
    self.options = options
    self.check_options()
    self.consumer = self.get_consumer()
    
  def check_options(self):
    if self.options.batch <= 0:
      raise ValueError('batch must be greater than 0')
    if self.options.wait_seconds <= 0:
      raise ValueError('wait_seconds must be greater than 0')
    if self.options.callback is None:
      raise ValueError('callback must be provided')
    if self.options.instance_id is None:
      raise ValueError('instance_id must be provided')
    if self.options.request_topic is None:
      raise ValueError('request_topic must be provided')
    if self.options.group_id is None:
      raise ValueError('group_id must be provided')
    if self.options.message_tag is None:
      raise ValueError('message_tag must be provided')
    
  def get_consumer(self):
    instance_id = self.options.instance_id
    message_tag = self.options.message_tag
    # 是否是静态 topic
    if self.options.is_static_topic:
      mq_topic = self.options.request_topic
    # 否则拼接 topic
    else:
      mq_topic = f"{self.options.env.upper()}_{self.options.appname.upper()}_{self.options.request_topic}"
      
    # 是否是静态 group
    if self.options.is_static_group:
      mq_group_id = self.options.group_id
    # 否则拼接 group
    else:
      mq_group_id = f"GID_{self.options.appname.upper()}_{self.options.group_id}_{self.options.env.upper()}"
      
    logger.info(f'mq_topic is {mq_topic}, mq_group_id is {mq_group_id}')
    return self.mq_client.get_consumer(instance_id, mq_topic, mq_group_id, message_tag)

  def run(self):
    batch = self.options.batch
    wait_seconds = self.options.wait_seconds
    logger.info(f'batch is {batch}, wait_seconds is {wait_seconds}')
    while True:
      try:
        recv_msgs = self.consumer.consume_message(batch, wait_seconds)
        # 直接 ack 消息
        try:
          receipt_handle_list = [msg.receipt_handle for msg in recv_msgs]
          self.consumer.ack_message(receipt_handle_list)
          logger.info(("Receive, Ack %s Message Succeed." % len(receipt_handle_list)))
        except Exception as e:
          logger.info(("Receive, Ack Message Fail! Exception:%s" % e))
        # 处理消息
        for msg in recv_msgs:
          self.handle_single_message(msg)
      except Exception as e:
        # 如果是消息不存在异常，忽略
        try:
          if e is not None and e.type == "MessageNotExist":
            continue
        except Exception:
          pass
        logger.info(("Consume Message Fail, but we just ignore! Exception:%s" % e))
        traceback_info = traceback.format_exc()
        logger.info(traceback_info)
        sleep(3)
      
  def handle_single_message(self, msg):
    """handle_single_message 处理单个消息

    Args:
        msg (_type_): consume_message 返回的消息
    """
    logger.info(("Receive, MessageId: %s MessageTag: %s" %
            (msg.message_id, msg.message_tag)))
    tag = msg.message_tag
    logger.info(f'tag is {tag}')
    payload_obj = safe_json_loads(msg.message_body)
    logger.info(f'payload_obj is {payload_obj}')
    payload: Payload = Payload(**payload_obj)
    payload.messageTag = tag
    result = self.options.callback(payload)
    logger.info(f'result is {result}')

class MQListener:
  def __init__(self, callback: Callable):
    instance_id = os.getenv('ROCKETMQ_INSTANCE_ID')
    topic = os.getenv('ROCKETMQ_BASE_REQUEST_TOPIC')
    group_id = os.getenv('ROCKETMQ_BASE_GROUP_ID')
    message_tag = os.getenv('ROCKETMQ_MESSAGE_TAG')
    endpoint = os.getenv('ROCKETMQ_ENDPOINT')
    access_key = os.getenv('ROCKETMQ_ACCESS_KEY')
    access_secret = os.getenv('ROCKETMQ_ACCESS_SECRET')
    is_static_topic = os.getenv('ROCKETMQ_STATIC_TOPIC')
    is_static_group = os.getenv('ROCKETMQ_STATIC_GROUP')
    env = os.getenv('ENV')
    appname = os.getenv('APPNAME')
    self.options = MQListenerOptions(
      instance_id=instance_id,
      request_topic=topic,
      group_id=group_id,
      message_tag=message_tag,
      callback=callback,
      endpoint=endpoint,
      access_key=access_key,
      access_secret=access_secret,
      env=env,
      appname=appname,
      is_static_topic=is_static_topic,
      is_static_group=is_static_group
    )

  def start(self):
    thread = MQListenerThread(self.options)
    thread.start()