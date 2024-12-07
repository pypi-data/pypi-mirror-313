import json
import os
import oss2
import base64
from io import BytesIO

from awe.util.logging import logger

oss_domain = os.getenv('OSS_DOMAIN')
access_key = os.getenv('OSS_ACCESS_KEY')
bucket_name = os.getenv('OSS_BUCKET')
access_secret = os.getenv('OSS_ACCESS_SECRET')

def get_bucket():
  auth = oss2.Auth(access_key, access_secret)
  return oss2.Bucket(auth, oss_domain, bucket_name)

def get_download_url(file_id, expires = 3600):
  logger.info(('bucket_name %s , file_id: %s , expires: %s' % (bucket_name, file_id, expires)))
  bucket = get_bucket()
  url = bucket.sign_url('GET', file_id, expires, params={})
  logger.info('oss file url is %s' % url)
  return url

def upload_file(inputstream: BytesIO, object_name):
  bucket = get_bucket()
  bucket.put_object(object_name, inputstream)
  return get_download_url(object_name)

def upload_base64_image(base64_str, object_name):
  inputstream = BytesIO(base64.b64decode(base64_str))
  return upload_file(inputstream, object_name)

def get_file_content(file_id):
  bucket = get_bucket()
  data = bucket.get_object(file_id).read();
  try:
    str_data = data.decode('utf-8')
    return json.loads(str_data)
  except Exception as e:
    logger.error('get_file_content error: %s' % e)
    return data