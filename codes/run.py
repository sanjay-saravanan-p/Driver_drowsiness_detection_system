import cv2
import winsound
import time
import threading
from drowsiness_core import DrowsinessDetector

alert_active = False
cap = cv2.VideoCapture(0)
detector = DrowsinessDetector()

def draw_eye(eye, frame):
    for (x, y) in eye:
        cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

    cv2.line(frame, tuple(eye[1]), tuple(eye[5]), (0, 0, 255), 1)  
    cv2.line(frame, tuple(eye[2]), tuple(eye[4]), (0, 0, 255), 1)  
    cv2.line(frame, tuple(eye[0]), tuple(eye[1]), (0, 255, 0), 1)
    cv2.line(frame, tuple(eye[1]), tuple(eye[2]), (0, 255, 0), 1)
    cv2.line(frame, tuple(eye[2]), tuple(eye[3]), (0, 255, 0), 1)
    cv2.line(frame, tuple(eye[3]), tuple(eye[4]), (0, 255, 0), 1)
    cv2.line(frame, tuple(eye[4]), tuple(eye[5]), (0, 255, 0), 1)
    cv2.line(frame, tuple(eye[5]), tuple(eye[0]), (0, 255, 0), 1)

alarm_running = False

def alarm_sound():
    global alarm_running
    while alarm_running:
        winsound.Beep(2000, 500)
        time.sleep(0.1)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    original_frame = frame.copy()



    drowsy, ear, left_eye, right_eye = detector.process_frame(frame)
    if left_eye is not None and right_eye is not None:
        draw_eye(left_eye, frame)
        draw_eye(right_eye, frame)


    if ear is not None:
        cv2.putText(frame, f"EAR: {ear:.2f}", (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,2 , 0), 2)

    if drowsy:
        cv2.putText(frame, "DROWSINESS ALERT!", (30, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        if not alarm_running:
            alarm_running = True
            threading.Thread(target=alarm_sound, daemon=True).start()
    else:
        alarm_running = False
    

    cv2.imshow("Driver Drowsiness Detection", frame)
    cv2.imshow("Original Camera Feed", original_frame)


    if cv2.waitKey(1) & 0xFF in (ord("q"), 27):
        break

cap.release()
cv2.destroyAllWindows()
