import torch
import cv2
from PIL import Image
import numpy as np
from yolov5.models.experimental import attempt_load
from yolov5.utils.general import non_max_suppression, scale_coords
from yolov5.utils.torch_utils import select_device


class YOLOv5Detector:
    def __init__(self, weights_path, conf=0.4, iou=0.5):
        self.model = attempt_load(weights_path, map_location=torch.device('cpu'))
        self.conf = conf
        self.iou = iou
        self.device = select_device('')
        
    def detect(self, img_path):
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = self.model.img_size[0], self.model.img_size[1]
        img = self.model.preprocess(img)
        img = torch.from_numpy(img).to(self.device)
        img = img.float()
        img /= 255.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        with torch.no_grad():
            detections = self.model(img)[0]
            detections = non_max_suppression(detections, self.conf, self.iou)
            if detections[0] is not None:
                detections = detections[0].cpu().numpy()
                detections[:, :4] = scale_coords(img.shape[2:], detections[:, :4], img.shape[2:]).round()

        return detections
