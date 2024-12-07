import os
import json
from pydantic import BaseModel, Field
from mq_http_sdk.mq_client import MQClient
from mq_http_sdk.mq_producer import TopicMessage

from awe.util.logging import logger
from awe.types.common import Payload, ResponseMessage
from awe.util.util import debounce

class MQProducerOptions(BaseModel):
  endpoint: str = Field(title="MQ Endpoint", description="MQ Endpoint", default="")
  access_key: str = Field(title="MQ Access Key", description="MQ Access Key", default="")
  access_secret: str = Field(title="MQ Access Secret", description="MQ Access Secret", default="")
  instance_id: str = Field(title="实例ID", description="实例ID", default="")
  is_static_topic: bool = Field(title="是否为静态Topic", description="是否为静态Topic", default=False)
  env: str = Field(title="环境", description="环境", default="")
  appname: str = Field(title="应用名", description="应用名", default="")
  response_topic: str = Field(title="响应Topic", description="响应Topic", default="")

class MQProducer:
  def __init__(self, options: MQProducerOptions = None):
    self.options = options or MQProducerOptions(
      endpoint=os.getenv('ROCKETMQ_ENDPOINT'),
      access_key=os.getenv('ROCKETMQ_ACCESS_KEY'),
      access_secret=os.getenv('ROCKETMQ_ACCESS_SECRET'),
      instance_id=os.getenv('ROCKETMQ_INSTANCE_ID'),
      is_static_topic=os.getenv('ROCKETMQ_STATIC_TOPIC'),
      env=os.getenv('ENV'),
      appname=os.getenv('APPNAME'),
      response_topic=os.getenv('ROCKETMQ_BASE_RESPONSE_TOPIC')
    )
    self.producer = self.get_producer(self.options)
    
  def get_producer(self, options: MQProducerOptions):
    mq_client = MQClient(
      options.endpoint,
      options.access_key,
      options.access_secret
    )
    if options.is_static_topic:
      producer_topic = options.response_topic
    else:
      topic_prefix = f"{options.env.upper()}_{options.appname.upper()}"
      producer_topic = f"{topic_prefix}_{options.response_topic}"
    
    logger.info(f'producer_topic is {producer_topic}')
    return mq_client.get_producer(options.instance_id, producer_topic)

  def send_progress_message(self, message: ResponseMessage, payload: Payload):
    message_body = {
      "code": "0",
      "status": "PROCESSING",
      "success": True,
      "taskId": payload.taskId,
      "userId": payload.userId,
      "clientId": payload.clientId,
      "client_id": payload.clientId,
      "appName": self.options.appname,
      "response": message.response,
      "workflowCode": payload.workflowCode
    }
    debounced = message.get("debounced")
    if debounced:
      self.debounce_progress_message(json.dumps(message_body), payload.messageTag)
    else:
      self.publish_message(json.dumps(message_body), tag=payload.messageTag)
    
  @debounce(0.1)
  def debounce_progress_message(self, message: str, tag: str):
    self.publish_message(message, tag)

  def send_error_message(self, message: ResponseMessage, payload: Payload):
    message_body = {
      "code": message.code if message.code else "500",
      "status": "FAILED",
      "success": False,
      "taskId": payload.taskId,
      "userId": payload.userId,
      "clientId": payload.clientId,
      "client_id": payload.clientId,
      "appName": self.options.appname,
      "response": message.response,
      "workflowCode": payload.workflowCode
    }
    self.publish_message(json.dumps(message_body), tag=payload.messageTag)

  def send_complete_message(self, message: ResponseMessage, payload: Payload):
    message_body = {
      "code": message.code if message.code else "0",
      "status": "SUCCEED",
      "success": True,
      "taskId": payload.taskId,
      "userId": payload.userId,
      "clientId": payload.clientId,
      "client_id": payload.clientId,
      "appName": self.options.appname,
      "workflowCode": payload.workflowCode,
      "response": message.response,
      "results": message.response['data'],
    }
    if payload.messageTag == 'WEB':
      message_body['results'] = []
    self.publish_message(json.dumps(message_body), tag=payload.messageTag)
  
  def publish_message(self, message: str, tag: str = None):
    try:
      topic_message = TopicMessage(message, tag)
      re_msg = self.producer.publish_message(topic_message)
      logger.info("Publish Succeed, TopicName:%s MessageID:%s MessageBody:%s" % (self.options.response_topic, re_msg.message_id, message))
    except Exception as e:
      logger.error("Publish, Message Fail. Exception:%s" % e)
