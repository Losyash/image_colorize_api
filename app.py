import os, PIL, cv2, base64
import numpy as np

from datetime import datetime
from io import BytesIO
from random import randint
from zipfile import ZipFile, ZIP_DEFLATED

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.deoldify import device
from src.deoldify.device_id import DeviceId
from src.deoldify.visualize import *
from src.app_utils import get_model_bin

os.environ["TORCH_HOME"] = os.path.join(os.getcwd(), ".cache")
os.environ["XDG_CACHE_HOME"] = os.path.join(os.getcwd(), ".cache")

device.set(device=DeviceId.CPU)

def load_model(model_dir, option):
  if option.lower() == 'artistic':
    model_url = 'https://data.deepai.org/deoldify/ColorizeArtistic_gen.pth'
    get_model_bin(model_url, os.path.join(model_dir, "ColorizeArtistic_gen.pth"))
    colorizer = get_image_colorizer(artistic=True)
  elif option.lower() == 'stable':
    model_url = "https://www.dropbox.com/s/usf7uifrctqw9rl/ColorizeStable_gen.pth?dl=0"
    get_model_bin(model_url, os.path.join(model_dir, "ColorizeStable_gen.pth"))
    colorizer = get_image_colorizer(artistic=False)

  return colorizer

def resize_img(input_img, max_size):
  img = input_img.copy()
  img_height, img_width = img.shape[0],img.shape[1]

  if max(img_height, img_width) > max_size:
    if img_height > img_width:
      new_width = img_width*(max_size/img_height)
      new_height = max_size
      resized_img = cv2.resize(img,(int(new_width), int(new_height)))
      return resized_img

    elif img_height <= img_width:
      new_width = img_height*(max_size/img_width)
      new_height = max_size
      resized_img = cv2.resize(img,(int(new_width), int(new_height)))
      return resized_img

  return img

def colorize_image(pil_image, img_size=800):
  pil_img = pil_image.convert("RGB")
  img_rgb = np.array(pil_img)
  resized_img_rgb = resize_img(img_rgb, img_size)
  resized_pil_img = PIL.Image.fromarray(resized_img_rgb)

  output_pil_img = colorizer.plot_transformed_pil_image(resized_pil_img, render_factor=35, compare=False)

  return output_pil_img

os.environ["TORCH_HOME"] = os.path.join(os.getcwd(), ".cache")
os.environ["XDG_CACHE_HOME"] = os.path.join(os.getcwd(), ".cache")

device.set(device=DeviceId.CPU)

st_color_option = "Artistic"
colorizer = load_model('models/', st_color_option)

class FileItem(BaseModel):
  file: str

class LinkItem(BaseModel):
  link: str

app = FastAPI()

origins = [
  'http://localhost',
  'http://localhost:5173'
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)

@app.post("/api/file")
async def from_file(file_item: FileItem):
  byte_data = base64.b64decode(file_item.file)
  img_input = PIL.Image.open(BytesIO(byte_data)).convert("RGB")

  img_output = colorize_image(img_input)
  img_output = img_output.resize(img_input.size)

  buffered = BytesIO()
  img_output.convert("RGB")
  img_output.convert("RGB").save(buffered, format="JPEG")
  img_str = base64.b64encode(buffered.getvalue())

  return img_str