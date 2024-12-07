import json
import os
import piexif
import base64
import requests
from PIL import Image
from io import BytesIO
from threading import Timer
from nanoid import generate
from datetime import datetime
from awe.util.logging import logger
from awe.oss import upload_file

def get_remote_json(url):
  return requests.get(url).json()

def get_remote_base64_image(url):
  if url is None:
    logger.error("URL is None, cannot get image.")
    return None
  if url.startswith("http"):
    # 向URL发送GET请求
    response = requests.get(url)
    # 确保请求成功
    if response.status_code == 200:
      # 从响应中获取图片数据作为二进制
      image_data = response.content
      # 创建一个BytesIO对象
      image_bytes = BytesIO(image_data)
      # 使用Pillow打开图片
      image = Image.open(image_bytes)
      # 创建一个新的BytesIO对象，这次用于保存base64编码的数据
      buff = BytesIO()
      # 保存图片到buff对象中（格式可以使用image.format来自动确定）
      image.save(buff, format=image.format)
      # 获取buff内的二进制数据
      byte_data = buff.getvalue()
      # 进行base64编码并解码为UTF-8字符串
      base64_str = base64.b64encode(byte_data).decode('utf-8')
      # 返回base64编码的图片数据
      return base64_str
    else:
      raise requests.exceptions.HTTPError(f"Failed to get image from {url}, Status Code: {response.status_code}")
  
  # 判断是否是 base64 编码的图片
  try:
    # 尝试解码base64字符串
    base64.b64decode(url)
    # 如果没有抛出异常，则是base64编码的图片
    return url
  except Exception as e:
    logger.error(f"URL is not valid, cannot get image. {e}")
    return None

def generate_filename_with_date(file_format):
  file_id = generate('1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 10)
  dir_path = datetime.now().strftime("%Y/%m/%d")
  return f"{dir_path}/{file_id}.{file_format}"

def get_file_extension(file_name):
  return file_name.split('.')[-1]

def create_dir_if_not_exists(directory):
  try:
    os.makedirs(directory, exist_ok=True)
    logger.info(f"确保目录 '{directory}' 存在。")
  except OSError as error:
    logger.error(f"创建目录时发生错误：{error}")
  return directory

def is_animated_webp(image):
  return getattr(image, 'is_animated', False)

def compress_png(image_path, output_path):
  try:
    # 打开图像文件
    with Image.open(image_path) as img:
      # 检查图像模式，如果是RGBA则转换为支持透明度的WebP
      if img.mode == 'RGBA':
        try:
          img.save(output_path, format='WEBP', lossless=True, transparency=img.info.get('transparency'))
        except Exception as e:
          img.save(output_path, format='WEBP')
      else:
        img.save(output_path, format='WEBP')
    print(f"转换成功，文件已保存至：{output_path}")
  except Exception as e:
    print(f"转换过程中发生错误：{e}")

def add_img_source(source_path, target_path, meta: dict):
  now = datetime.now().strftime("%Y:%m:%d %H:%M:%S")
  img_description = meta.get("description", "")
  img_artist = meta.get("artist", "")
  img_software = meta.get("software", "")
  img_copyright = meta.get("copyright", "")
  img_datetime = meta.get("DateTime", now)
  img_datetime_original = meta.get("DateTimeOriginal", now)
  comment = f"{img_description}\n{img_artist}\n{img_software}\n{img_copyright}"
  
  exif_info = {
    "0th": {
      piexif.ImageIFD.ImageDescription: comment,
      piexif.ImageIFD.Artist: img_artist,
      piexif.ImageIFD.Software: img_software,
      piexif.ImageIFD.Copyright: img_copyright,
      piexif.ImageIFD.DateTime: img_datetime,
    },
    "Exif": {
      piexif.ExifIFD.DateTimeOriginal: img_datetime_original,
    }
  }

  # 试图把EXIF信息转为字节流
  try:
      exif_bytes = piexif.dump(exif_info)
      if exif_bytes is not None:
        # 读取图片
        img = Image.open(source_path)
        # 把EXIF信息写入图片
        img.save(target_path, exif=exif_bytes)
  except ValueError as e:
      print(f"遇到错误：{e}")
      exif_bytes = b""

def upload_remote_image(url, params, path, file_extension='png'):
  IMAGE_META_COPYRIGHT = os.getenv("IMAGE_META_COPYRIGHT")
  IMAGE_META_ARTIST = os.getenv("IMAGE_META_ARTIST")
  IMAGE_META_SOFTWARE = os.getenv("IMAGE_META_SOFTWARE")
  IMAGE_META_DESCRIPTION = os.getenv("IMAGE_META_DESCRIPTION")
  try:
    logger.info(f"upload_remote_image: {url}")
    content = requests.get(url, params=params).content
    # 视频或音频不压缩
    if file_extension == 'mp4' or file_extension == 'webm' or file_extension == 'mp3':
      logger.info(f"upload_remote_image: {path} is video, no compression")
      return path, upload_file(content, path)
    image = Image.open(BytesIO(content))
    logger.info(f"image.mode: {image.mode}")
    # 动图不压缩
    if is_animated_webp(image):
      logger.info(f"upload_remote_image: {path} is animated webp, no compression")
      return path, upload_file(content, path)
    else:
      logger.info(f"upload_remote_image: {path} is image, compressing")
      dir_path = "output/" + "/".join(path.split("/")[:-1])
      create_dir_if_not_exists(dir_path)
      temp_file_path = "output/" + path
      if image.mode == 'RGBA':
        logger.info(f"upload_remote_image: {path} is RGBA, converting to webp")
        try:
          image.save(temp_file_path, format='PNG', lossless=True, transparency=image.info.get('transparency'))
        except Exception as e:
          logger.error(f'upload_remote_image failed: {e}')
          image.save(temp_file_path, format='PNG')
      else:
        image.save(temp_file_path, format='PNG')
      # image.save(temp_file_path)
      temp_webp_path = temp_file_path.split(".")[0] + ".webp"
      compress_png(temp_file_path, temp_webp_path)
      now = datetime.now().strftime("%Y:%m:%d %H:%M:%S")
      add_img_source(temp_webp_path, temp_webp_path, {
        "description": IMAGE_META_DESCRIPTION,
        "artist": IMAGE_META_ARTIST,
        "software": IMAGE_META_SOFTWARE,
        "copyright": IMAGE_META_COPYRIGHT,
        "DateTimeOriginal": now,
        "DateTime": now
      })
      new_content = open(temp_webp_path, "rb").read()
      new_path = path.split(".")[0] + ".webp"
    return new_path, upload_file(new_content, new_path)
  except Exception as e:
    logger.error(f'upload_remote_image failed: {e}')
    return path, upload_file(content, path)
  
def debounce(wait_time):
    def decorator(func):
        def debounced_function(*args, **kwargs):
            def call_it():
                debounced_function.timer = None
                return func(*args, **kwargs)
            
            if debounced_function.timer is not None:
                debounced_function.timer.cancel()
            debounced_function.timer = Timer(wait_time, call_it)
            debounced_function.timer.start()
        
        debounced_function.timer = None
        return debounced_function
    return decorator
  
def upload_image_to_comfyui(upload_url, filename, image_url):

  # 下载图片
  response = requests.get(image_url)
  image_data = response.content

  dir_path = datetime.now().strftime("%Y-%m-%d")
  file_id = generate('1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 10)
  filename = f'{dir_path}-{file_id}-{filename}'

  # 准备 multipart/form-data 请求体
  files = {
      'image': (filename, image_data, 'image/png'),
      'subfolder': (None, ''),
      'type': (None, 'input')
  }

  # 发送 POST 请求上传图片
  resp = requests.post(upload_url, files=files)

  # 检查响应
  if resp.ok:
      res = resp.json()
      logger.info(f'Image uploaded successfully: {res}')
      return res
  else:
      raise Exception(f'Failed to upload image: {resp.text}')
      
def safe_json_loads(json_str):
  try:
    return json.loads(json_str)
  except Exception as e:
    logger.error(f'safe_json_loads failed: {e}')
    return None