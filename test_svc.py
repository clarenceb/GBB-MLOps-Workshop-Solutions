# Posts a base64 encoded image to the WebService for testing the scoring.

import argparse
import requests
import os, json, base64
from io import BytesIO
import urllib.request
import io
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument("scoring_uri")
parser.add_argument("image_path")
parser.add_argument("key")
args = parser.parse_args()

def imgToBase64(img):
    """Convert pillow image to base64-encoded image"""
    imgio = BytesIO()
    img.save(imgio, 'JPEG')
    img_str = base64.b64encode(imgio.getvalue())
    return img_str.decode('utf-8')

base64Img = imgToBase64(Image.open(args.image_path))
data = {'data':base64Img}
headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + args.key}
    
# Sending post request and saving response as response object 
r = requests.post(url=args.scoring_uri, data=json.dumps(data), headers=headers)
print(r.json())