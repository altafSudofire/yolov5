from glob import glob
import boto3
from conf import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION_NAME
from send_number_to_server import *
textractclient = boto3.client("textract", aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION_NAME)
import codecs
import re
import os
import time
import glob

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

print("GET IMAGES FROM PATH")
# img_lst = glob('runs/detect/exp43/crops/number-plate/*')
# img_lst.sort()

def on_file_created(event, image_list):
    if event.src_path.endswith('.jpg'):
        new_image = event.src_path
        image_list.append(new_image)
        print("New image added:", new_image)

def watch_images_folder(path):
    image_list = glob.glob(path + '/*.jpg')

    def handle_event(event):
        nonlocal image_list
        if event.is_directory:
            return
        elif event.event_type == 'created':
            on_file_created(event, image_list)

    event_handler = FileSystemEventHandler()
    event_handler.on_any_event = handle_event

    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

    return image_list

watch_images_folder('runs/detect/exp43/crops/number-plate/')
updated_image_list = watch_images_folder('runs/detect/exp43/crops/number-plate/')

print("Updated image list:", updated_image_list)

def read_num(img_lst=img_lst, client=textractclient):
    # file =open("./image_4.jpeg", encoding="utf8")
    # with open("./video3.jpeg", 'rb') as f:
    rto_code_list = ['AP',  'AR',  'AN',  'CG',  'DN',  'GA',  'HP',  'JK',  'KL',  'MP',  'ML',  'LD',  'NL',  'OD',  'SK',  'TN',
                 'UK',  'AS',  'BR',  'CH',  'GJ',  'DD',  'HR',  'JH',  'KA',  'MH',  'MN',  'MZ',  'DL',  'PY',  'PB',  'RJ',  'TR',  'UP']
    txt_lst = []
    num = 0
    max_num = ''
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
                    # print(block)
                    # print('\033[94m' + item["Text"] + '\033[0m')
                    extractedText = extractedText+block["Text"]
                    # extractedText = extractedText.replace(' ', '')[-10:]
            responseJson = {
                "text": extractedText
            }
            # import ipdb;ipdb.set_trace()
            print(responseJson, type(responseJson))
            os.remove(img)
            # txt_lst.append(num++ + '---' +img)
            if responseJson["text"] != '':
                if responseJson["text"] != max_num:
                    txt_lst.append(responseJson["text"])
            if len(txt_lst) == 10:
                if responseJson["text"] == txt_lst[-2]:
                    print("txt_lst > 10 and last element same, max: ", max(set(txt_lst), key = lambda x: txt_lst.count(x)))
                    max_num = max(set(txt_lst), key = lambda x: txt_lst.count(x))
                    print(max_num)
                    txt_lst.clear()
                else:
                    print("txt_lst >10 and last element different, max: ",max(set(txt_lst), key = lambda x: txt_lst.count(x)))
                    max_num = max(set(txt_lst), key = lambda x: txt_lst.count(x))
                    txt_lst.clear()
                    print("text_list is cleared, max_num: ", max_num)
                print("return max: ", max_num)
                record = filter_num(max_num)
                print(f"{record['number']} is successfully published to client")
                # send(MQTT_USER, MQTT_PASS, record)
    if 1<len(txt_lst)<=10:
        print("txt_lst between 1 to 10, max: ", max(set(txt_lst), key = lambda x: txt_lst.count(x)))
        max_num = max(set(txt_lst), key = lambda x: txt_lst.count(x))
    else:
        print("txt_lst is single or 0 element, txt_lst: ", txt_lst)
        max_num = txt_lst
    print("all cases are false, txt_lst: ", txt_lst)
    print(max_num)
    record = filter_num(max_num)
    print(f"{record['number']} is successfully published to client")
    # send(MQTT_USER, MQTT_PASS, record)

def filter_num(txt):
    print("---text list", txt)
    if txt is not None:
        flt_txt = re.sub(r'[^a-zA-Z0-9]', '', txt)
    if flt_txt[:3].lower() == 'ind':
        re.sub(r'.','', flt_txt, count = 3)
    # flt_lst = [x for x in flt_lst if x[0].isalnum()]
    # flt_lst = [re.sub(r'.', '', x, count = 5) for x in flt_lst if x[:3] == 'IND']
    # flt_lst = [x for x in flt_lst if x[:2] in rto_code_list]
    # if len(cleaned_text) >= 6 and cleaned_text[:2] in rto_code_list:
    #                 extracted_list.append(cleaned_text[-10:])
    return {
        "device": "stream",
        "number": flt_txt
    }