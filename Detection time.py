import os
import torch
from ultralytics import YOLO
import torchvision.transforms as transforms
from PIL import Image
import time

# Load YOLOv8 model
model = YOLO('D:/train9/weights/best.pt')

# Define image transformations
transform = transforms.Compose([
    transforms.Resize((416, 416)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Specify the folder containing images
folder_path = "E:/Final Year_Pro/New folder"

# Get all image file names in the folder
image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

# Load images
images = [Image.open(os.path.join(folder_path, f)) for f in image_files]

# Apply transformations
inputs = [transform(image).unsqueeze(0) for image in images]

# Start time
start_time = time.time()

# Detection loop
with torch.no_grad():
    for input_img in inputs:
        output = model(input_img)

# End time
end_time = time.time()

# Calculate total time
total_time = end_time - start_time
print("Total detection time:", total_time, "seconds")
