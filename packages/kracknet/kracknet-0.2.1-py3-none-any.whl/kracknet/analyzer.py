import os
import json
import requests
from .utils.dataclass import DataClass, UnknownOption
from .utils.decorators import ensure_retry
from .utils import config
from .prediction import BasePrediction

class TaskConfigurationError (Exception):
  pass

class HttpResponseError (Exception):
  pass

class BaseAnalyzer:
  TASK_TYPE = None
  PREDICTION_CLASS = BasePrediction
  PREDICTION_RETRY = 3

  def __init__ (self, backend = None, access_key = None):
    assert self.TASK_TYPE is not None
    self.config = config.get_config (backend, access_key)
    self.backend = self.config.server.backend
    self.access_key = self.config.server.access_key
    self.fetch_options ()

  def calibrate_options (self, data):
    for op in data ['options']:
      if op ['key'] == 'road_length_m':
        del op ['default']

  def before_reuqest (self, thresholds, options):
    return thresholds, options

  def after_reuqest (self, response):
    return response

  def predict (self, img_path):
    if img_path.startswith ('s3://'):
      from rs4.apis.aws import s3
      local_path = os.path.join ('/tmp', os.path.basename (img_path))
      s3.download (img_path, local_path)
      assert os.path.isfile (local_path)
      img_path = local_path
    return self._predict (img_path)

  def check_response (self, r):
    if not (200 <= r.status_code < 300):
      err = r.json ()
      raise HttpResponseError (f'{r.status_code} {r.reason}, code:{err ["code"]} message:{err ["message"]}')

  @ensure_retry (PREDICTION_RETRY)
  def _predict (self, img_path):
    self.options.validate ()
    thresholds = self.thresholds.get_value ()
    options = self.options.get_value ()
    thresholds, options = self.before_reuqest (thresholds, options)

    data = {
      'threshold': json.dumps (thresholds),
      'options': json.dumps (options),
      'image_name': os.path.basename (img_path),
      'task_type': self.TASK_TYPE
    }
    files = {'image': open (img_path, 'rb')}
    r = requests.post (
      f'{self.backend}/apis/tasks/cli/outputs', data = data, files = files,
      headers = {'Authorization': f'Bearer {self.access_key}'}
    )
    self.check_response (r)
    assert r.status_code == 201, f'status code: {r.status_code}'
    response = r.json ()
    response = self.after_reuqest (response)
    return self.PREDICTION_CLASS (img_path, response)

  def save_configuration (self, out_path):
    data = {
      'task_type': self.TASK_TYPE,
      'setting': {
        'options': self.options.asdict (ignore_unset = True),
        'thresholds': self.thresholds.asdict (ignore_unset = True)
      }
    }
    with open (out_path, 'w') as f:
      f.write (json.dumps (data, indent = 2))

  def load_configuration (self, json_path):
    if isinstance (json_path, dict):
      data = json_path
    else:
      with open (json_path) as f:
        data = json.loads (f.read ())
    if data ['task_type'] != self.TASK_TYPE:
      raise TaskConfigurationError (f'mismatched task type')
    data ['setting']['threshold'] = data ['setting'].pop ('thresholds')
    self.apply_configuration (data ['setting'])

  def load_configuration_from_task (self, task_id):
    r = requests.get (f'{self.backend}/apis/settings/{task_id}', headers = {'Authorization': f'Bearer {self.access_key}'})
    self.check_response (r)
    data = r.json ()
    if data ['task_type'] != self.TASK_TYPE:
      raise TaskConfigurationError (f'mismatched task type')
    conf = json.loads (data ['setting'])
    self.apply_configuration (conf)

  def apply_configuration (self, conf):
    for k, v in conf ['options'].items ():
      try: setattr (self.options, k, v)
      except UnknownOption: pass

    try:
      disabled = conf ['threshold'].pop ('__disabled__')
    except KeyError:
      disabled = {}

    for k, v in conf ['threshold'].items ():
      if k in disabled or v == 100:
        v = -1
      try: setattr (self.thresholds, k, v)
      except UnknownOption: pass

  def fetch_options (self):
    r = requests.get (f'{self.backend}/apis/codes', params = {'task_type': self.TASK_TYPE, 'exclude_hidden': 'no'})
    self.check_response (r)
    data = r.json ()
    self.calibrate_options (data)

    valid_options = []
    for op in data ['options']:
      if op.get ('type') == 'boolean':
        op ['type'] = 'bool'
      if op.get ('deprecated') or op.get ('noneed'):
        continue
      valid_options.append (op)
    self.options = DataClass (valid_options)

    thresholds = []
    for op in data ['codes']:
      if op.get ('deprecated') or op.get ('noneed'):
        continue
      if not op ['enabled']:
        op ['default'] = -1
      thresholds.append ({
          'key': op ['code'], 'default': op ['default'], 'valid_range': [-1, 99],
          'name': op ['full_name'], 'type': 'int', 'color': tuple ([int (op ['color'] [i: i +2], 16) for i in range (0, 6, 2)])
      })
    self.thresholds = DataClass (thresholds)
    self.PREDICTION_CLASS.set_code_infos (self.options, self.thresholds)

  def get_summary (self):
    raise NotImplementedError
