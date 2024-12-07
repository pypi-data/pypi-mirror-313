
class ComfyUIException(Exception):
  def __init__(self, message, node_id=None, node_type=None):
    self.message = message
    self.node_id = node_id
    self.node_type = node_type
    
  def __str__(self):
    return f"{self.message}, node_id: {self.node_id}, node_type: {self.node_type}"
  
