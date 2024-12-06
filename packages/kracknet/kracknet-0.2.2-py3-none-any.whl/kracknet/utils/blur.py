import cv2
import numpy as np

def masked_blur (img, mask, blur_ksize, iteration = 1, ksize = 3, use_gausian = True, sigma = 1):
  if blur_ksize % 2 == 0:
    blur_ksize += 1
  ksize = max (int (blur_ksize * 0.3), 3)
  blur = cv2.blur (img, (blur_ksize, blur_ksize))
  final_img = img.copy ().astype (float)
  mask = mask.astype (float)
  for _ in range (iteration):
    alpha = mask / 255.
    final_img = (alpha [:, :, None] * blur) + ((1 - alpha) [:, :, None] * final_img)
    if use_gausian:
      mask = cv2.GaussianBlur (mask, (ksize, ksize), sigma)
    else:
      mask = cv2.blur (mask, (ksize, ksize))
  return final_img.clip (0, 255.0).astype (np.uint8)

def blurring (frame, results, blur_ksize = 21, mask_only = False):
  img_h, img_w = frame.shape [:2]
  c_mask = np.zeros ((img_h, img_w), np.uint8)
  for idx, r in enumerate (results):
    shape = r ['shape_type']
    points = r ['points']
    if shape == 'polygon':
      cv2.fillConvexPoly (c_mask, np.array (points), 255, lineType = cv2.LINE_AA)
    else:
      cv2.ellipse (c_mask, points [0], points [1], 0, 0, 360, 255, -1, lineType = cv2.LINE_AA)
  if mask_only:
    return c_mask
  final_img = masked_blur (frame, c_mask, blur_ksize, iteration = 2, ksize = 3, use_gausian = False)
  return final_img
