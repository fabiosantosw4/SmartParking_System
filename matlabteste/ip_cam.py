import cv2
import torch
import os
import random

from matplotlib import pyplot as plt


model = torch.hub.load('ultralytics/yolov5', 'custom', 'best.pt')


os.makedirs('cropped_cars', exist_ok=True)

def detect_cars_on_ip_camera(camera_url):
    cap = cv2.VideoCapture(camera_url)
    count = 0
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        results = model(frame)
        cars = results.pandas().xyxy[0][results.pandas().xyxy[0]['name'] == 'car']
        
        for index, car in cars.iterrows():
            xmin, ymin, xmax, ymax = int(car['xmin']), int(car['ymin']), int(car['xmax']), int(car['ymax'])
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            
            
            car_image = frame[ymin:ymax, xmin:xmax]
            
            
            image_id = random.randint(0, 9999)
            
            
            cv2.imwrite(f'cropped_cars/car_{image_id}.jpg', car_image)
        
        cv2.imshow('IP Camera', frame)
        
        if cv2.waitKey(1) == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


camera_url = 'http://211.132.61.124/mjpg/video.mjpg'


detect_cars_on_ip_camera(camera_url)
