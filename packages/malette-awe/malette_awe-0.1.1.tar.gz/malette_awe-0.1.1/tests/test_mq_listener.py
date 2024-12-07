import pytest
from unittest.mock import patch, MagicMock
from awe.mq.mq_listener import MQListener, MQListenerThread
from awe.types.common import Payload

def test_mq_listener_init():
    """测试 MQ 监听器初始化"""
    callback = MagicMock()
    listener = MQListener(callback=callback)
    assert listener.options.callback == callback

@patch('awe.mq.mq_listener.MQClient')
def test_mq_listener_start(mock_mq_client):
    """测试 MQ 监听器启动"""
    mock_client = MagicMock()
    mock_mq_client.return_value = mock_client
    
    callback = MagicMock()
    listener = MQListener(callback=callback)
    listener.start()
    
    assert listener.thread is not None
    assert listener.thread.is_alive()

def test_handle_single_message():
    """测试单条消息处理"""
    callback = MagicMock()
    listener = MQListener(callback=callback)
    
    # 创建模拟消息
    mock_msg = MagicMock()
    mock_msg.message_body = '{"taskId": "123", "api": "test"}'
    mock_msg.message_tag = "test_tag"
    
    # 处理消息
    thread = MQListenerThread(options=listener.options)
    thread.handle_single_message(mock_msg)
    
    # 验证回调被调用
    callback.assert_called_once()
    args = callback.call_args[0][0]
    assert isinstance(args, Payload)
    assert args.taskId == "123"
    assert args.messageTag == "test_tag" 