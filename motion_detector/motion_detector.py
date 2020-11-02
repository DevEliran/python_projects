from imutils.video import VideoStream
from datetime import datetime
import pandas
import imutils
import time
import cv2

first_frame = None
status_list = [None, None]
times = []
df = pandas.DataFrame(columns=["Start", "End"])
video = VideoStream(src=0).start()
time.sleep(2.0)

while True:
    frame = video.read()
    status = 0
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame,
                        cv2.COLOR_BGR2GRAY)  # Conversion from RGB to gray scale
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if first_frame is None:
        first_frame = gray  # first frame is 'frame' on a gray scale
        continue

    delta_frame = cv2.absdiff(first_frame, gray)
    thresh_frame = cv2.threshold(delta_frame, 25, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    contours = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    for contour in contours:
        if cv2.contourArea(
                contour) < 7500:  # looking for moving areas with a contour greater than 7500px
            continue
        status = 1
        (x, y, w, h) = cv2.boundingRect(
            contour)  # drawing a rectangle around the moving object
        cv2.rectangle(frame, (x, y), (x + w, y + h), (230, 255, 0), 3)
    status_list.append(status)
    # status_list contains only two values . if these values are different a time stamp will be added to the dataframe
    status_list = status_list[-2:]
    # status is either 1 or 0 ; 1 - moving object in frame ; 0- moving object not in frame
    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())

    cv2.imshow("Threshold", thresh_frame)
    cv2.imshow("delta", delta_frame)
    cv2.imshow("Capturing", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        if status == 1:  # in case user pressed q to quit and there is a moving object in the frame
            times.append(datetime.now())
        break

for i in range(0, len(times), 2):
    df = df.append({"Start": times[i], "End": times[i + 1]},
                   ignore_index=True)  # inserting data to the dataframe

df.to_csv("time_log.csv")
video.stop()
cv2.destroyAllWindows()
