# Driver Drowsiness Detection System using MediaPipe and OpenCV

This project is a Python-based real-time driver drowsiness detection system that uses
a webcam and facial landmark detection to monitor eye behavior and alert the driver
when prolonged eye closure is detected.

The system focuses on explainable computer vision techniques rather than black-box
machine learning models.


## Features

- Real-time face and eye detection using webcam
- Eye Aspect Ratio (EAR) based drowsiness detection
- Visual eye landmark points and EAR reference lines
- Continuous audio alert using laptop inbuilt speaker
- Dual camera view:
  - Original raw camera feed
  - Processed feed with eye visualization and alerts
- Clean and minimal 2-file project structure


## Technologies Used

- Python
- OpenCV
- MediaPipe Face Mesh
- NumPy
- Winsound (for audio alert on Windows)
- Threading (for non-blocking sound alert)


## Project Structure

Driver_Drowsiness_Detection/

- codes/
   -drowsiness_core.py   # Core detection logic (EAR, landmarks, state).
   -run.py               # Execution, visualization and sound alert.
   
- README.md
- requirements.txt


## How to Run
1. Install the required libraries
2. Ensure a working webcam is connected
3. Run the main script

Press **Q** or **ESC** to exit the application.


## Drowsiness Detection Logic (Important)

This project does NOT use machine learning model training.

Drowsiness detection is performed using geometric analysis of eye landmarks.

Eye Aspect Ratio (EAR):
- Eye landmarks are extracted using MediaPipe Face Mesh.
- Two vertical eye distances and one horizontal eye distance are measured.
- EAR is calculated as:

EAR = (A + B) / (2 × C)

Where:
- A, B represent vertical eyelid distances
- C represents horizontal eye width

As the eyes close:
- Vertical distances reduce significantly
- EAR value drops below a predefined threshold

If the EAR remains below the threshold for consecutive frames,
the driver is considered drowsy.


## Alert Logic

- Normal blinking is ignored using frame-based logic
- If eyes remain closed continuously:
  - A warning message is displayed on screen
  - A continuous beep alert is played using the laptop speaker
- The alert stops immediately once the eyes reopen

Audio alert runs in a separate thread to avoid freezing the video feed.


## Usage Notes

For best performance:
- Ensure the driver's face is clearly visible
- Maintain a well-lit environment
- Avoid extreme head rotations
- Position the camera at eye level
- Use a stable camera setup


## Limitations

- Performance may degrade in low-light conditions
- Designed for single-driver detection
- Detects eye closure, not medical fatigue or sleep disorders


## Future Improvements
- Yawning detection using mouth landmarks
- Low-light and night-time robustness
- Alert escalation based on duration
- Hardware buzzer or vibration motor integration
- Video recording of detection output
- Mobile or embedded deployment (ESP32 / Raspberry Pi)

<!------------------------------------------------------>

## Privacy Notice

This repository does NOT store or collect any personal data.

All webcam frames are processed only in real time and are NOT saved.
No images, videos, or facial data are stored on disk.

Do NOT upload recorded camera frames, screenshots, or personal images
to GitHub to protect user privacy.
