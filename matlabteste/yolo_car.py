import torch
import cv2
import os

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', 'best.pt')

# Set video input
video_path = 'video3.mp4'

# Open video file
cap = cv2.VideoCapture(video_path)

# Create directory to save license plate images
os.makedirs('license_plates', exist_ok=True)

# Initialize counter for saving images
image_counter = 0

# Set confidence threshold for saving license plates
confidence_threshold = 0.89

while cap.isOpened():
    # Read frame from the video
    ret, frame = cap.read()
    if not ret:
        break

    # Perform object detection
    results = model(frame)

    # Parse results
    for detection in results.xyxy[0]:
        x1, y1, x2, y2, conf, cls = detection
        label = model.names[int(cls)]
        
        if label == 'license_plate' and conf >= confidence_threshold:
            # Crop and save the license plate image
            plate_img = frame[int(y1):int(y2), int(x1):int(x2)]
            output_path = f'license_plates/plate_{image_counter}.jpg'
            cv2.imwrite(output_path, plate_img)
            image_counter += 1

        # Draw bounding box and label
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(frame, f'{label} {conf:.2f}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    # Display the resulting frame
    cv2.imshow('YOLOv5 Object Detection', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
