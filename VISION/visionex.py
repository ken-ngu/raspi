import io
import os

from google.cloud import vision
from google.cloud.vision import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="\home\pi\Vision-5c3fdde91350.json"
vision_client = vision.ImageAnnotatorClient()
file_name = 'image.jpg'

with io.open(file_name,'rb') as image_file:
     content = image_file.read()

     image = types.Image(content=content)

     response = vision_client.label_detection(image=image)
     labels = response.label_annotations

     for label in labels:
          print(label.description)
