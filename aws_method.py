from glob import glob
import boto3
from conf import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION_NAME
from send_number_to_server import *
textractclient = boto3.client("textract", aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION_NAME)
import cv2
import codecs
import re
import os
import time
from collections import Counter
import glob
from PIL import Image
import io

img_lst = glob.glob('runs/detect/exp54/crops/number-plate/*')

def read_num(img_lst=img_lst, client=textractclient):
    rto_code_list = ['AP',  'AR',  'AN',  'CG',  'DN',  'GA',  'HP',  'JK',  'KL',  'MP',  'ML',  'LD',  'NL',  'OD',  'SK',  'TN',
                 'UK',  'AS',  'BR',  'CH',  'GJ',  'DD',  'HR',  'JH',  'KA',  'MH',  'MN',  'MZ',  'DL',  'PY',  'PB',  'RJ',  'TR',  'UP']
    txt_lst = []
    num = 0
    max_num = ''
    # watch_images_folder('runs/detect/exp43/crops/number-plate')
    for img in img_lst:
        print("image name: ", img)
        with open(img, 'rb') as f:
            binaryFile = f.read()
            response = textractclient.detect_document_text(
                Document={
                    'Bytes': binaryFile
                }
            )
            extractedText = ""
            for block in response['Blocks']:
                if block["BlockType"] == "LINE":
                    extractedText = extractedText+block["Text"]
                    # extractedText = extractedText.replace(' ', '')[-10:]
            responseJson = {
                "text": extractedText
            }
            print(responseJson, type(responseJson))
            if responseJson["text"] != '':
                if responseJson["text"] != max_num:
                    txt_lst.append(responseJson["text"])

    print(txt_lst)
    max_num = max(set(txt_lst), key = lambda x: txt_lst.count(x))
    txt_lst.clear()
    for img in img_lst:
        os.remove(img)
    record = filter_num(max_num)
    print(f"{record['vehicle_number']} is successfully published to client")
    # send(MQTT_USER, MQTT_PASS, record)

def filter_num(txt):
    print("---text list", txt)
    if txt is not None:
        flt_txt = re.sub(r'[^a-zA-Z0-9]', '', txt)
    if flt_txt[:3].lower() == 'ind':
        re.sub(r'.','', flt_txt, count = 3)
    return flt_txt
# read_num()

def read_single_image_num(img, textract_client=textractclient):
    # Load the image using OpenCV
    # image = cv2.imread(img)

    # Convert the image to PIL format
    image_pil = Image.fromarray(img)

    # Convert PIL image to byte stream
    byte_stream = io.BytesIO()
    image_pil.save(byte_stream, format='JPEG')
    byte_stream.seek(0)

    # Call the Textract API to extract text from the image
    response = textract_client.detect_document_text(Document={'Bytes': byte_stream.read()})

    extracted_text = ""
    for block in response['Blocks']:
        if block["BlockType"] == "LINE":
            extracted_text += block["Text"]

    responseJson = {
        "text": extracted_text
    }
    filtered_text = filter_num(responseJson["text"])
    # print(responseJson, type(responseJson))
    return filtered_text