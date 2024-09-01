import cv2
import mediapipe as mp
import numpy as np

# Initialize Mediapipe Pose
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Open the webcam
cap = cv2.VideoCapture(0)

def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

exercise = input("Choose your exercise (Bicep Curls, Shoulder Press, Lateral Raises): ").strip().lower()

# Setup Mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    counter_curls = 0
    counter_shoulder_press = 0
    counter_lateral_raises = 0
    stage_curls = None
    stage_shoulder_press = None
    stage_lateral_raises = None

    while cap.isOpened():
        ret, frame = cap.read()

        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detection
        results = pose.process(image)

        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark

            # Get coordinates
            shoulder_l = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow_l = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist_l = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            shoulder_r = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow_r = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            wrist_r = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

            hip_l = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            hip_r = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

            # Calculate angles
            angle_curl_l = calculate_angle(shoulder_l, elbow_l, wrist_l)
            angle_curl_r = calculate_angle(shoulder_r, elbow_r, wrist_r)
            angle_shoulder_press_l = calculate_angle(hip_l, shoulder_l, elbow_l)
            angle_shoulder_press_r = calculate_angle(hip_r, shoulder_r, elbow_r)
            angle_lateral_raises_l = calculate_angle(hip_l, shoulder_l, wrist_l)
            angle_lateral_raises_r = calculate_angle(hip_r, shoulder_r, wrist_r)

            # Curl counter logic
            if exercise == "bicep curls":   
                if angle_curl_l > 160 and angle_curl_r > 160:
                    stage_curls = "down"
                if angle_curl_l < 30 and angle_curl_r < 30 and stage_curls == 'down':
                    stage_curls = "up"
                    counter_curls += 1
                    print("Curls:", counter_curls)

            # Shoulder press logic
            if exercise == "shoulder press":
                if angle_shoulder_press_l < 100 and angle_shoulder_press_r < 100:
                    stage_shoulder_press = "down"
                if angle_shoulder_press_l > 160 and angle_shoulder_press_r > 160 and stage_shoulder_press == 'down':
                    stage_shoulder_press = "up"
                    counter_shoulder_press += 1
                    print("Shoulder Presses:", counter_shoulder_press)

            # Lateral raises logic
            if exercise == "lateral raises":
                if angle_lateral_raises_l < 10 and angle_lateral_raises_r < 10:
                    stage_lateral_raises = "down"
                if angle_lateral_raises_l > 80 and angle_lateral_raises_r > 80 and stage_lateral_raises == 'down':
                    stage_lateral_raises = "up"
                    counter_lateral_raises += 1
                    print("Lateral Raises:", counter_lateral_raises)

        except:
            pass

        # Render curl counter
        cv2.rectangle(image, (0, 0), (225, 100), (245, 117, 16), -1)
        cv2.putText(image, 'BICEP CURLS', (15, 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter_curls),
                    (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

        # Render shoulder press counter
        cv2.rectangle(image, (0, 100), (225, 200), (245, 117, 16), -1)
        cv2.putText(image, 'SHOULDER PRESS', (15, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter_shoulder_press),
                    (10, 170),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

        # Render lateral raises counter
        cv2.rectangle(image, (0, 200), (225, 300), (245, 117, 16), -1)
        cv2.putText(image, 'LATERAL RAISES', (15, 220),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter_lateral_raises),
                    (10, 270), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
