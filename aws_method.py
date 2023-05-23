from glob import glob
import boto3
from conf import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION_NAME

textractclient = boto3.client("textract", aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION_NAME)
import codecs
import re

print("GET IMAGES FROM PATH")
img_lst = glob('runs/detect/exp43/crops/number-plate/*')
img_lst.sort()
print(img_lst, type(img_lst))

def read_num(img_lst=img_lst, client=textractclient):
    # file =open("./image_4.jpeg", encoding="utf8")
    # with open("./video3.jpeg", 'rb') as f:
    rto_code_list = ['AP',  'AR',  'AN',  'CG',  'DN',  'GA',  'HP',  'JK',  'KL',  'MP',  'ML',  'LD',  'NL',  'OD',  'SK',  'TN',
                 'UK',  'AS',  'BR',  'CH',  'GJ',  'DD',  'HR',  'JH',  'KA',  'MH',  'MN',  'MZ',  'DL',  'PY',  'PB',  'RJ',  'TR',  'UP']
    txt_lst = []
    num = 0
    for img in img_lst:
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
            # txt_lst.append(num++ + '---' +img)
            txt_lst.append(responseJson["text"])
            if len(txt_lst) == 10:
                if responseJson["text"] == txt_lst[-2]:
                    print("txt_lst > 10 and last element same, max: ", max(set(txt_lst), key = lambda x: txt_lst.count(x)))
                    max_num = max(set(txt_lst), key = lambda x: txt_lst.count(x))
                    print(max_num)
                    continue
                else:
                    print("txt_lst >10 and last element different, max: ",max(set(txt_lst), key = lambda x: txt_lst.count(x)))
                    max_num = max(set(txt_lst), key = lambda x: txt_lst.count(x))
                    print(max_num)
                print("return max: ", max_num)
                return max_num
    if 1<len(txt_lst)<=10:
        print("txt_lst between 1 to 10, max: ", max(set(txt_lst), key = lambda x: txt_lst.count(x)))
        max_num = max(set(txt_lst), key = lambda x: flt_lst.count(x))
    else:
        print("txt_lst is single or 0 element, txt_lst: ", txt_lst)
        max_num = txt_lst
    print("all cases are false, txt_lst: ", txt_lst)
    print(max_num)
    return max_num

read_num()