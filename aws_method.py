from glob import glob
import boto3
from conf import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION_NAME

textractclient = boto3.client("textract", aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION_NAME)
import codecs


print("GET IMAGES FROM PATH")
img_lst = glob('detected_images/*')
img_lst.sort()
print(img_lst, type(img_lst))

def read_num():
    # file =open("./image_4.jpeg", encoding="utf8")
    # with open("./video3.jpeg", 'rb') as f:
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
            txt_lst.append(num++ + '---' +img)
            txt_lst.append(responseJson["text"])

    print(txt_lst)