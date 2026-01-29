import cv2
import mediapipe as mp
import numpy as np

EAR_THRESHOLD = 0.25
FRAME_LIMIT = 20

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
# -----------------------------------------------------------------------------------

mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(refine_landmarks=True)

def eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    return (A + B) / (2.0 * C)

class DrowsinessDetector:
    def __init__(self):
        self.counter = 0

    def process_frame(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = face_mesh.process(rgb)

        drowsy = False
        ear_value = None

        if result.multi_face_landmarks:
            face = result.multi_face_landmarks[0]
            h, w, _ = frame.shape

            left_eye, right_eye = [], []

            for idx in LEFT_EYE:
                lm = face.landmark[idx]
                left_eye.append([int(lm.x * w), int(lm.y * h)])

            for idx in RIGHT_EYE:
                lm = face.landmark[idx]
                right_eye.append([int(lm.x * w), int(lm.y * h)])

            left_eye = np.array(left_eye)
            right_eye = np.array(right_eye)

            ear = (eye_aspect_ratio(left_eye) +
                   eye_aspect_ratio(right_eye)) / 2.0

            ear_value = ear

            if ear < EAR_THRESHOLD:
                self.counter += 1
                if self.counter >= FRAME_LIMIT:
                    drowsy = True
            else:
                self.counter = 0

        return drowsy, ear_value, left_eye if result.multi_face_landmarks else None, right_eye if result.multi_face_landmarks else None
