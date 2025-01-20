import base64
from io import BytesIO
from PIL import Image

# Pillow to base64
def pil_to_base64(pil_img):
  img_buffer = BytesIO()
  pil_img.save(img_buffer, format='JPEG')
  byte_data = img_buffer.getvalue()
  base64_str = base64.b64encode(byte_data)
  return base64_str