import cv2
import glob
import os
import requests
import json
import sys

from django.shortcuts import render
from django.db import connection


cam = cv2.VideoCapture(0)

count = 0
while True:
    ret, img = cam.read()
    cv2.imshow("test", img)

    if not ret:
        break

    k = cv2.waitKey(1)

    if k % 256 == 27:
        print("close")
        break
    elif k % 256 == 32:

        file = 'G:/Projects/Django/final_year_project/Rwanda_police/media/capture/img' + str(count) + '.jpg'
        cv2.imwrite(file, img)
        count += 1
        break

regions = ['in']

with open(r'G:\Projects\Django\final_year_project\Rwanda_police\media\capture\img0.jpg', 'rb') as fp:
    response = requests.post('https://api.platerecognizer.com/v1/plate-reader/',
                             data=dict(regions=regions),
                             files=dict(upload=fp),
                             headers={'Authorization': 'Token 0289f9a7b72ddc46be7f23375b5217e4fd40b2bc'})

plate_number = response.json()['results'][0]['plate']
plate_number_a = response.json()
print("plate-------------------", plate_number_a)


print("plate number is : " + plate_number.upper())

cv2.waitKey(0)
cam.release()
cv2.destroyAllWindows()

# code when we have more than plate number ============================
# regions = ['in']
#
# with open(r'G:\Projects\Django\final_year_project\Rwanda_police\media\capture\img0.PNG', 'rb') as fp:
#     response = requests.post('https://api.platerecognizer.com/v1/plate-reader/',
#                              data=dict(regions=regions),
#                              files=dict(upload=fp),
#                              headers={'Authorization': 'Token 0289f9a7b72ddc46be7f23375b5217e4fd40b2bc'})
#
# plate_number = response.json()['results'][0]['plate']
# plate_number_a = response.json()
# # print("plate-------------------", plate_number_a['results'])
# for plate in plate_number_a['results']:
#     plate_num = plate['plate']
#     print("plate number is : " + plate_num.upper())