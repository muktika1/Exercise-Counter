# Exercise Counter using Mediapipe

## Project Overview

This project is a real-time exercise counter utilizing Mediapipe's Pose Detection. It helps track and count three types of exercises: Bicep Curls, Shoulder Presses, and Lateral Raises. By analyzing the live webcam feed, it provides real-time feedback on the number of repetitions performed for each exercise.

## Features

- **Real-Time Exercise Counting:** Detects and counts Bicep Curls, Shoulder Presses, and Lateral Raises using a live webcam feed.
- **Pose Detection:** Uses Mediapipe's Pose module to track and analyze body landmarks.
- **Dynamic Display:** Displays exercise counts and real-time feedback directly on the video feed.

## How It Works

1. **Pose Detection:** The system uses Mediapipe to detect body landmarks from the webcam feed.
2. **Angle Calculation:** Calculates angles between body joints to determine the position of the arms and shoulders during exercises. 
   - **Bicep Curls:** Measures the angle between the shoulder, elbow, and wrist to detect curl movements.
   - **Shoulder Presses:** Uses the angle between the shoulder, elbow, and hip to track the shoulder press movement.
   - **Lateral Raises:** Measures the angle between the shoulder, elbow, and wrist for lateral raises.
3. **Counting Logic:** Updates counts based on the detected positions and angles, providing real-time feedback on repetitions.

## Getting Started

### Prerequisites

- Python 3.x
- Mediapipe
- OpenCV
- NumPy


## Usage

1. **Start the Program:** Run `python3 exercise_counter.py` to start the application.
2. **Choose Exercise:** Input the exercise you want to track (Bicep Curls, Shoulder Press, Lateral Raises).
3. **Perform the Exercise:** Follow the instructions and perform the selected exercise. The count will be displayed in real-time on the video feed.
4. **Stop the Application:** Press `q` to quit the program.

## Angle Calculations

- **Angle Calculation:** The angle between three points (A, B, C) is calculated using the arctangent function to determine the orientation of the body parts during exercise. This angle helps in identifying the position of arms and shoulders, essential for accurate counting.
