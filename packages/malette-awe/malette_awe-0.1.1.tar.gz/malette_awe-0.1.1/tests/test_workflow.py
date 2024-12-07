import pytest
from unittest.mock import patch, MagicMock
from awe.util.workflow import contains_chinese, translate, get_workflow_data
from awe.types.common import Payload

def test_contains_chinese():
    """测试中文检测"""
    assert contains_chinese("你好") == True
    assert contains_chinese("Hello") == False
    assert contains_chinese("Hello你好") == True
    assert contains_chinese("") == False

@patch('awe.util.workflow.tongyi_translate')
def test_translate(mock_translate):
    """测试翻译功能"""
    mock_translate.return_value = "beautiful girl"
    
    # 测试中文翻译
    result = translate("漂亮的女孩")
    assert result == "beautiful girl"
    mock_translate.assert_called_once_with("漂亮的女孩")
    
    # 测试英文不翻译
    result = translate("beautiful girl")
    assert result == "beautiful girl"

def test_get_workflow_data():
    """测试获取工作流数据"""
    # 测试直接包含workflow的情况
    payload = Payload(
        taskId="123",
        workflow={"test": "data"}
    )
    result = get_workflow_data(payload)
    assert result == {"test": "data"}
    
    # 测试空workflow的情况
    payload = Payload(taskId="123")
    result = get_workflow_data(payload)
    assert result is None 