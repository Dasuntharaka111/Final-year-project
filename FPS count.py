import pandas as pd
import time
import cv2
from ultralytics import YOLO
from Counting_track import *
import cvzone

# Load YOLO model
model = YOLO('D:/train4/weights/best.pt')

# Use Mouse function for adjust the cv2 lines according to case
def CV2_line_adjuster(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        point = [x, y]
        print(point)

cv2.namedWindow("Okra_Pods_Detection")
cv2.setMouseCallback("Okra_Pods_Detection", CV2_line_adjuster)

# Open video file
cap = cv2.VideoCapture(0)

# Open Okra_class.txt file for reading class labels and Split class labels into a list
my_file = open("E:/Final Year_Pro/Okra_class.txt", "r")
data = my_file.read()
class_list = data.split("\n")

threshold = 0.47  # Threshold for object detection confidence
count = 0  # Counter for frame iteration
cy1=745  # Initial y-coordinate for the line
offset=15  # Offset for line

# Initialize trackers for two classes
tracker1 = Tracker()
tracker2 = Tracker()

# Initialize lists to store IDs of detected objects
counter1 = []
counter2 = []

# Variables for calculating FPS
start_time = time.time()
frame_count = 0

# Main loop to process each frame of the video
while True:
    # Read frame from the video
    ret, frame = cap.read()

    # Break the loop if no frame is retrieved
    if not ret:
        break

    # Increment frame count and process every third frame
    frame_count += 1
    if frame_count % 3 != 0:
        continue

    # Resize the frame
    frame = cv2.resize(frame, (1020, 500))

    # Perform object detection using YOLO
    results = model(frame)[0]

    # Extract bounding box coordinates and class labels
    a = results.boxes.data
    px = pd.DataFrame(a).astype("float")

    # Initialize lists to store bounding boxes and class labels
    list1 = []
    Can_Emus = []
    list2 = []
    Cant_Emus = []

    # Iterate over each detected object
    for index, row in px.iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])
        c = class_list[d]

        # Group objects based on class labels
        if 'CE' in c:
            list1.append([x1, y1, x2, y2])
            Can_Emus.append(c)
        elif "NE" in c:
            list2.append([x1, y1, x2, y2])
            Cant_Emus.append(c)

    # Update trackers with bounding box coordinates
    bbox1_idx = tracker1.update(list1)
    bbox2_idx = tracker2.update(list2)

    # Visualize and count Can Emasculate pods
    for bbox1 in bbox1_idx:
        for i in Can_Emus:
            x3, y3, x4, y4, id1 = bbox1
            cxm = int(x3 + x4) // 2
            cym = int(y3 + y4) // 2
            if cxm<(cy1+offset) and cxm>(cy1-offset):
                cv2.circle(frame, (cxm, cym), 4, (255, 255, 255), -1)
                if counter1.count(id1) == 0:
                    counter1.append(id1)
            else:
                for result in results.boxes.data.tolist():
                    x1, y1, x2, y2, score, class_id = result
                    print(class_id)
                    if score > threshold:
                        object_detection()

    # Visualize and count Cant Emasculate pods
    for bbox2 in bbox2_idx:
        for h in Cant_Emus:
            x5,y5,x6,y6,id2 = bbox2
            cxc = int(x5 + x6) // 2
            cyc = int(y5 + y6) // 2
            if cxc<(cy1+offset) and cxc>(cy1-offset):
                cv2.circle(frame, (cxc, cyc), 4, (255,255, 255), -1)
                if counter2.count(id2) == 0:
                    counter2.append(id2)
            else:
                for result in results.boxes.data.tolist():
                    x1, y1, x2, y2, score, class_id = result
                    print(class_id)
                    if score > threshold:
                        object_detection()

    # object detection function
    def object_detection():
        if 0.0 == class_id:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)
        elif 1.0 == class_id:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 4)
            cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)
        elif 2.0 == class_id:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 4)
            cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
        elif 3.0 == class_id:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 4)
            cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)

    # Draw a line on the frame
    cv2.line(frame, (cy1,1), (cy1,498), (0, 0, 255), 2)

    # Calculate and display counts of detected objects
    Can_Emus_lec = (len(counter1))
    Cant_Emus_lec = (len(counter2))
    total_pods = Can_Emus_lec+Cant_Emus_lec
    cvzone.putTextRect(frame, f'Can Emasculation:-{Can_Emus_lec}', (19, 30), 2, 1)
    cvzone.putTextRect(frame, f"Can't Emasculation:-{Cant_Emus_lec}", (18, 71), 2, 1)
    cvzone.putTextRect(frame, f"Total Pods:-{total_pods}", (16, 115), 2, 1)

    # Calculate FPS
    elapsed_time = time.time() - start_time
    fps = frame_count / elapsed_time

    # Display FPS
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 170), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Display the frame
    cv2.imshow("Okra_Pods_Detection", frame)

    # Break the loop if 'Esc' key is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release video capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
