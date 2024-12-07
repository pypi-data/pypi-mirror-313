import pytest
from unittest.mock import patch, MagicMock
from awe.awe.awe import AWE

def test_awe_init():
    """测试 AWE 初始化"""
    awe = AWE(comfyui_host="localhost", comfyui_port="8188")
    assert awe.comfyui_host == "localhost"
    assert awe.comfyui_port == "8188"

@patch('awe.awe.awe.ComfyUIClient')
@patch('awe.awe.awe.MQListener')
@patch('awe.awe.awe.MQProducer')
def test_awe_start(mock_producer, mock_listener, mock_client, mock_env):
    """测试 AWE 启动流程"""
    # 准备模拟对象
    mock_client_instance = MagicMock()
    mock_listener_instance = MagicMock()
    mock_producer_instance = MagicMock()
    
    mock_client.return_value = mock_client_instance
    mock_listener.return_value = mock_listener_instance
    mock_producer.return_value = mock_producer_instance
    
    # 初始化并启动 AWE
    awe = AWE(comfyui_host="localhost", comfyui_port="8188")
    awe.start()
    
    # 验证调用
    mock_client_instance.connect.assert_called_once()
    mock_listener_instance.start.assert_called_once()
    mock_client_instance.on_progress.assert_called_once()
    mock_client_instance.on_error.assert_called_once()
    mock_client_instance.on_complete.assert_called_once() 