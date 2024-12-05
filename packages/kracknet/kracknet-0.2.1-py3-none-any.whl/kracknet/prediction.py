import json
import cv2
import numpy as np

class BasePrediction:
  @classmethod
  def set_code_infos (cls, options, thresholds):
    cls.options = options
    cls.thresholds = thresholds

  def __init__ (self, img_path, response):
    self.img_path = img_path
    self.response = response
    self.result = json.loads (self.response.pop ('result'))

  def __iter__ (self):
    for it in self.result ['shapes']:
      yield it

  def json (self):
    r = self.response.copy ()
    r ['result'] = self.result
    if '__spec__' in r:
      del r ['__spec__']
    return r

  def save_json (self, path):
    r = self.json ()
    with open (path, 'w') as f:
      f.write (json.dumps (r, indent = 2))

  def get_credit_balance (self):
    return self.response ['credit_balance']

  def get_result (self):
    return self.result

  def get_image (self) -> cv2.typing.MatLike:
    return cv2.imread (self.img_path)

  def plot (self, show_label = True) -> cv2.typing.MatLike:
    im = cv2.imread (self.img_path)
    for it in self:
      self.draw (im, it, show_label = show_label)
    return im

  def draw (self, im, d, show_label = True):
    points = np.reshape (d ['points'], (-1, 2)).astype (int)
    label = '{} {:.2f}'.format (d ["label"], d ['score'])
    line_color = self.thresholds.get_spec (d ["label"]) ['color']
    shape = d ['shape_type']
    current_line_width = 2
    if "severity" in d:
      current_line_width = {'Critical': 3, 'Major': 2, 'Minor': 1} [d ["severity"]]
    zoom_factor = (im.shape [0] / 1080)
    current_line_width = int (current_line_width * zoom_factor)

    if shape == 'rectangle':
      cv2.rectangle (im, points [0], points [1], line_color, current_line_width)
      text_pos = [points [0][0], points [0][1] - 10]
    elif shape in ('linestrip', 'polygon'):
      cv2.polylines (im, np.array ([points]), True if shape == 'polygon' else False, line_color, current_line_width, cv2.LINE_AA)
      if shape == 'linestrip':
        text_pos = [points [0][0], points [0][1] - 10]
      else:
        x1, y1 = np.min (points, 0).tolist ()
        text_pos = [x1, y1 - 10]
    elif shape == 'ellipse':
      cv2.ellipse (im, points [0], points [1], 0, 0, 360, line_color, current_line_width, lineType = cv2.LINE_AA)
      x1, y1 = [points [0][0] - points [1][0], points [0][1] - points [1][1]]
      text_pos = [x1, y1 - 10]
    else:
      raise ValueError (f'Unknown shape {d ["shape_type"]}')

    if show_label:
      cv2.rectangle (im, (text_pos [0] - int (1 * zoom_factor), text_pos [1] - int (9 * zoom_factor)), (text_pos [0] + int (80 * zoom_factor), text_pos [1] + int (5 * zoom_factor)), 64, -1)
      cv2.rectangle (im, (text_pos [0] - int (4 * zoom_factor), text_pos [1] - int (12 * zoom_factor)), (text_pos [0] + int (80 * zoom_factor), text_pos [1] + int (5 * zoom_factor)), line_color, -1)
      cv2.putText (im, label, text_pos, cv2.FONT_HERSHEY_PLAIN, 0.7 * zoom_factor, (255, 255, 255), int (1 * zoom_factor), cv2.LINE_AA)
