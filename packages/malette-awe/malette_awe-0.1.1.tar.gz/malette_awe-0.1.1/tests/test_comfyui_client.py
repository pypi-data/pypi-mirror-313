import pytest
from unittest.mock import patch, MagicMock
from awe.clients.comfyui_client import ComfyUIClient

def test_comfyui_client_init():
    """测试 ComfyUI 客户端初始化"""
    client = ComfyUIClient("localhost", "8188")
    assert client.host == "localhost"
    assert client.port == "8188"
    assert client.status == "INIT"

@patch('websocket.WebSocket')
def test_comfyui_client_connect(mock_websocket):
    """测试 WebSocket 连接"""
    mock_ws = MagicMock()
    mock_websocket.return_value = mock_ws
    
    client = ComfyUIClient("localhost", "8188")
    client.connect()
    
    mock_ws.connect.assert_called_once()
    assert client.ws is not None

def test_comfyui_client_progress():
    """测试进度计算"""
    client = ComfyUIClient("localhost", "8188")
    
    # 测试空节点列表
    client.current_total_node_ids = []
    assert client.get_progress() == 1
    
    # 测试正常进度计算
    client.current_total_node_ids = ["1", "2", "3", "4"]
    client.current_executed_node_ids = ["1", "2"]
    assert client.get_progress() == 50
    
    # 测试进度为0的情况
    client.current_executed_node_ids = []
    assert client.get_progress() == 1  # 应该返回1而不是0 