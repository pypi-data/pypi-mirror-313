from functools import wraps
from rs4 import logger
import time
import logging
import sys

def ensure_retry (retry):
  def decorator(f):
    @wraps(f)
    def wrapper (analyzer, img_path):
      logging.info (f'predict {img_path}')
      n = retry + 1
      while n:
        try:
          return f (analyzer, img_path)
        except:
          n -= 1
          if not n:
            logging.error (logger.traceback ())
            raise
          t, v, tb = sys.exc_info ()
          logging.warning (f'{t.__name__}, retrying...')
          time.sleep (1)
    return wrapper
  return decorator