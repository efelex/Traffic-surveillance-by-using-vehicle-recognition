import cv2
import glob
import os
import requests
import json
import sys
import time
import numpy as np

classFile = r'G:\Projects\Django\final_year_project\Rwanda_police\car_plate\yolo_file\coco.names'
classNames = []
confThreshold = 0.5
nmsThreshold = 0.3
whT = 320
count = 0


def plate_detect():
    cam = cv2.VideoCapture(0)

    count = 0
    while True:
        ret, img = cam.read()
        cv2.imshow("Traffic surveillance", img)
        if not ret:
            break
        k = cv2.waitKey(1)
        if cv2.waitKey(1) == ord('q'):
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

    try:
        plate_number = response.json()['results'][0]['plate']
        plate_number_a = response.json()
    except:
        plate_number = 'dummy'
    # print("plate-------------------", plate_number_a)
    #
    # print("plate number is : " + plate_number.upper())

    cv2.waitKey(0)
    cam.release()
    cv2.destroyAllWindows()
    return plate_number.upper()


def findObjects(outputs, img):
    hT, wT, cT = img.shape
    bbox = []  # containing the x,y,w,h
    classIds = []  # all the class ids
    confs = []  # confidence values
    count = 0

    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                w, h = int(det[2] * wT), int(det[3] * hT)
                x, y = int((det[0] * wT) - w / 2), int((det[1] * hT) - h / 2)
                bbox.append([x, y, w, h])
                classIds.append(classId)
                confs.append(float(confidence))
    # here we are having the problem of having more box in one object so what we are going to do is to try to remove it
    indices = cv2.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold)
    print(indices)
    for i in indices:
        print("i=", i)
        # i = i[0]
        print("i=", i)
        box = bbox[i]
        # print("bbox[i]", bbox[i])
        car_det = classNames[classIds[i]].upper()
        print("car -------------------detected -------------------------", car_det)
        confidence_car = int(confs[i] * 100)
        if car_det == 'CAR' or car_det == 'TRUCK' and confidence_car > 60:
            x, y, w, h = box[0], box[1], box[2], box[3]
            # cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
            # cv2.putText(img, f'{classNames[classIds[i]].upper()} {int(confs[i]*100)}%', (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255.0,255), 2)

            file = 'G:/Projects/Django/final_year_project/Rwanda_police/media/automatic/img0.jpg'
            cv2.imwrite(file, img)
            # count += 1
            return 'car_detected'
        else:
            x, y, w, h = box[0], box[1], box[2], box[3]
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
            cv2.putText(img, f'{classNames[classIds[i]].upper()} {int(confs[i]*100)}%', (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255.0,255), 2)
            status_warning = 'NoneCar'
            return status_warning


def automatic_detect():
    cap = cv2.VideoCapture(0)
    with open(classFile, 'rt') as f:
        global classNames
        classNames = f.read().rstrip('\n').split('\n')
    modeConfiguration = 'G:\\Projects\\Django\\final_year_project\\Rwanda_police\\car_plate\\yolo_file\\yolov3-tiny.cfg'
    modelWeights = 'G:\\Projects\\Django\\final_year_project\\Rwanda_police\\car_plate\\yolo_file\\yolov3-tiny.weights'
    net = cv2.dnn.readNetFromDarknet(modeConfiguration, modelWeights)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    while True:
        success, img = cap.read()

        blob = cv2.dnn.blobFromImage(img, 1 / 255, (whT, whT), [0, 0, 0], 1, crop=False)
        net.setInput(blob)

        layerNames = net.getLayerNames()
        # print(layerNames)
        # print(net.getUnconnectedOutLayers())
        outputNames = [layerNames[i - 1] for i in net.getUnconnectedOutLayers()]
        # print(outputNames)
        outputs = net.forward(outputNames)
        findObjects(outputs, img)
        file_plate = findObjects(outputs, img)
        print("plate xxx --------------------", file_plate)
        cv2.imshow("Traffic surveillance", img)
        cv2.waitKey(1)
        k = cv2.waitKey(1)
        if cv2.waitKey(1) == ord('q'):
            break
        if file_plate is None:
            findObjects(outputs, img)
        elif file_plate == 'NoneCar':
            findObjects(outputs, img)
        else:
            regions = ['in']
            with open(r'G:\Projects\Django\final_year_project\Rwanda_police\media\automatic\img0.jpg', 'rb') as fp:

                response = requests.post('https://api.platerecognizer.com/v1/plate-reader/',
                                         data=dict(regions=regions),
                                         files=dict(upload=fp),
                                         headers={'Authorization': 'Token 0289f9a7b72ddc46be7f23375b5217e4fd40b2bc'})
            try:
                plate_number = response.json()['results'][0]['plate']
                plate_number_a = response.json()


            except:
                plate_number = 'dummy'
            return plate_number.upper()


