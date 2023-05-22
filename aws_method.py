from glob import glob
import boto3
from conf import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION_NAME

textractclient = boto3.client("textract", aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION_NAME)
import codecs
import re

print("GET IMAGES FROM PATH")
img_lst = glob('detected_images/*')
img_lst.sort()
print(img_lst, type(img_lst))

def read_num(img_lst, client=textractclient):
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
            print(responseJson, type(responseJson))
            # txt_lst.append(num++ + '---' +img)
            txt_lst.append(responseJson["text"])
    flt_lst = []
    for text in txt_list:
        if text is not None:
            s = re.sub(r'[^a-zA-Z0-9]', '', text)
            flt_lst.append(s)
    flt_lst = [x for x in flt_lst if x[0].isalnum()]
    flt_lst = [re.sub(r'.', '', x, count = 5) for x in flt_lst if x[:3] == 'IND']
    # flt_lst = [x for x in flt_lst if x[:2] in rto_code_list]
    if len(cleaned_text) >= 6 and cleaned_text[:2] in rto_code_list:
                    extracted_list.append(cleaned_text[-10:])
    if len(flt_lst) >1:
        res = max(set(flt_list), key = lambda x: flt_lst.count(x))
        return res
    print(flt_lst[0])
    return flt_lst[0]