# import cv2
# from matplotlib import pyplot as plt
# import numpy as np
# import imutils
# import easyocr

# img = cv2.imread('./input_images/image_12.jpg')
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# # plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))
# # plt.imshow(img)
# bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
# edged = cv2.Canny(bfilter, 30, 200) #Edge detection
# # plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))
# keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# contours = imutils.grab_contours(keypoints)
# contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
# location = None
# for contour in contours:
#     approx = cv2.approxPolyDP(contour, 10, True)
#     if len(approx) == 4:
#         location = approx
#         break
# mask = np.zeros(gray.shape, np.uint8)
# new_image = cv2.drawContours(mask, [location], 0,255, -1)
# new_image = cv2.bitwise_and(img, img, mask=mask)
# plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))
# (x,y) = np.where(mask==255)
# (x1, y1) = (np.min(x), np.min(y))
# (x2, y2) = (np.max(x), np.max(y))
# cropped_image = gray[x1:x2+1, y1:y2+1]
# plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
# ax=plt.gca()
# ax.get_yaxis().set_visible(False)
# ax.get_xaxis().set_visible(False)
# plt.savefig("output234.jpeg")
from glob import glob
import boto3
textractclient = boto3.client("textract", aws_access_key_id="AKIAX7P7MNX73OSRRGMM",
                              aws_secret_access_key="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", region_name="ap-south-1")
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