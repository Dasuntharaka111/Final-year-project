import cv2
import pandas as pd
from ultralytics import YOLO
from Counting_track import *
import cvzone
from pyfirmata import Arduino, SERVO, util
from time import sleep

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
cap = cv2.VideoCapture(1)

# Open Okra_class.txt file for reading class labels and Split class labels into a list
my_file = open("E:/Final Year_Pro/Okra_class.txt", "r")
data = my_file.read()
class_list = data.split("\n")

port = 'COM3'
pin0 = 2  # actuator servo
board = Arduino(port)
board.digital[pin0].mode = SERVO
angle0 = 0
i = True  # Assuming i is defined and initialized in your complete code
direction = 1  # 1 for moving down, -1 for moving up
speed = 1

threshold = 0.1  # Threshold for object detection confidence
count = 0  # Counter for frame iteration
k = 0

# Initialize trackers for two classes
tracker1 = Tracker()
tracker2 = Tracker()

# Initialize lists to store IDs of detected objects
counter1 = []
counter2 = []

board.digital[pin0].write(90)

def rotationservo(angle):
      global angle0
      board.digital[pin0].write(angle)

# Main loop to process each frame of the video
while True:
    # Read frame from the video
    ret, frame = cap.read()

    # Break the loop if no frame is retrieved
    if not ret:
        break

    # Increment frame count and process every third frame
    count += 1
    if count % 3 != 0:
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
    blade = []

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
        elif "SB" in c:
            list2.append([x1, y1, x2, y2])
            blade.append(c)

    # Update trackers with bounding box coordinates
    bbox1_idx = tracker1.update(list1)
    bbox2_idx = tracker2.update(list2)

    # Visualize the Can Emasculate pods
    for bbox1 in bbox1_idx:
        for i in Can_Emus:
            x3, y3, x4, y4, id1 = bbox1
            cv2.line(frame, (x3, 1), (x3, 498), (0, 0, 255), 2)
            cv2.line(frame, (x3-5, 1), (x3-5, 498), (0, 0, 255), 2)
            cv2.line(frame, (1, y3), (1020, y3), (0, 0, 255), 2)

            for result in results.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = result
                caller()
                print(class_id)
                if score > threshold:
                    object_detection()

    # Visualize the Blade and Execute cutting process
    for bbox2 in bbox2_idx:
        for h in blade:
            x5,y5,x6,y6,id2 = bbox2
            cxc = int(x5 + x6) // 2
            cyc = int(y5 + y6) // 2
            cv2.line(frame, (x6, 1), (x6, 498), (0, 0, 255), 2)
            cv2.line(frame, (x5+10, y6), (x6-10, y6), (0, 0, 255), 2)
            cv2.line(frame, (x6, 1), (x6, 498), (0, 0, 255), 2)

            #Execute Cutting Process
            def caller():
             if x3 >0:
              if x6 > (x3-10):
                cv2.circle(frame, (cxc, cyc), 4, (255, 255, 255), -1)
                rotationservo(97)
              if (y3+50) > y6:
                cv2.circle(frame, (cxc, cyc), 4, (255, 0, 255), -1)
                rotationservo(90)
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

    # Display the frame
    cv2.imshow("Okra_Cutter", frame)

    # Break the loop if 'Esc' key is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release video capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()