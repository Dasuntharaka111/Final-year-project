import cv2
import pandas as pd
from ultralytics import YOLO
import matplotlib.pyplot as plt
from collections import defaultdict
import time

model = YOLO('D:/train4/weights/best.pt')

cv2.namedWindow('RGB')
cap = cv2.VideoCapture('C:/New folder/FJVID_20240317_180515 (1).mp4')

my_file = open("E:/Final Year_Pro/Okra_class.txt", "r")
data = my_file.read()
class_list = data.split("\n")

# For storing confidence levels and timestamps
confidence_data = defaultdict(list)

# Start time in seconds
start_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (1020, 500))

    results = model(frame)[0]
    a = results.boxes.data
    px = pd.DataFrame(a).astype("float")

    list1 = []
    paper = []

    for index, row in px.iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])
        c = class_list[d]
        if 'CE' in c:
            list1.append([x1, y1, x2, y2])
            paper.append(c)

            # Store confidence level along with timestamp in seconds
            confidence_data['Can Emasculation'].append(row[4])
            confidence_data['timestamp'].append(time.time() - start_time)  # Convert to seconds

    # Display frame
    cv2.imshow("RGB", frame)

    # Plotting the graph
    if len(confidence_data['Can Emasculation']) > 1:
        plt.plot(confidence_data['timestamp'], confidence_data['Can Emasculation'])
        plt.xlabel('Time (seconds)')  # Update x-axis label
        plt.ylabel('Confidence Level')
        plt.title('Confidence Level Variation Over Time (Can Emasculation)')
        plt.draw()
        plt.pause(0.01)
        plt.clf()

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
