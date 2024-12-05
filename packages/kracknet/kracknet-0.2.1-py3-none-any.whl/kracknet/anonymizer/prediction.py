import os
import json
import numpy as np
import cv2
from rs4.annotations import override
from ..prediction import BasePrediction
from ..utils import blur

class Prediction (BasePrediction):
  @override
  def get_summary (self):
    summary = []
    for k, v in self.result ['summary'].items ():
      summary.append ({
        'type': k,
        'metric': 'Count',
        'unit': None,
        'value': v
      })
    return summary

  def mask (self) -> cv2.typing.MatLike:
    im = cv2.imread (self.img_path)
    return blur.blurring (im, self, mask_only = True)

  def blur (self) -> cv2.typing.MatLike:
    im = cv2.imread (self.img_path)
    return blur.blurring (im, self, self.options.blur_intensity)
