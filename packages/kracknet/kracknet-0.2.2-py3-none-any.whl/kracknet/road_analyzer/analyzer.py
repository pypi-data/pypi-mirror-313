from rs4.annotations import override
from ..analyzer import BaseAnalyzer
from .prediction import Prediction

class RoadScanImageAnalyzer (BaseAnalyzer):
  TASK_TYPE = 0
  PREDICTION_CLASS = Prediction

  @override
  def calibrate_options (self, data):
    super ().calibrate_options (data)
    for op in data ['options']:
      if op ['key'] in ('camera_height_m', 'focal_length_mm'):
        op ['noneed'] = True

  @override
  def before_reuqest (self, thresholds, options):
    thresholds ['CPJ2AR'] = thresholds ['CPJ3AR']= thresholds ['CPJ1AR']
    thresholds ['CPF2LN'] = thresholds ['CPF3LN']= thresholds ['CPF1LN']
    return thresholds, options

  @override
  def predict (self, img_path) -> Prediction:
    return super ().predict (img_path)

class DashCamImageAnalyzer (BaseAnalyzer):
  TASK_TYPE = 1
  PREDICTION_CLASS = Prediction

  @override
  def calibrate_options (self, data):
    super ().calibrate_options (data)
    for op in data ['options']:
      if op ['key'] in ('camera_height_m', 'focal_length_mm'):
        del op ['default']
      if op ['key'] in ('include_left_lane_line', 'include_right_lane_line'):
        del op ['name']

  @override
  def predict (self, img_path) -> Prediction:
    return super ().predict (img_path)