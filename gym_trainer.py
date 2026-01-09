# gym_trainer.py - AI Powered Fitness Rep Counter
import cv2
import mediapipe as mp
import numpy as np
from collections import deque
import time

# MediaPipe Pose Detection
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

class ExerciseDetector:
    def __init__(self):
        self.push_up_counter = 0
        self.squat_counter = 0
        self.pull_up_counter = 0
        self.plank_time = 0
        self.start_time = None
        
        # State tracking for different exercises
        self.push_up_down = False
        self.squat_down = False
        self.pull_up_down = False
        self.plank_started = False
        
        # Smoothing buffer for stability
        self.angle_buffer = deque(maxlen=5)
    
    def calculate_angle(self, a, b, c):
        """Calculate angle between three points"""
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        
        ba = a - b
        bc = c - b
        
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
        angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
        return np.degrees(angle)
    
    def detect_push_up(self, landmarks):
        """Detect push-up exercise"""
        # Get relevant joints
        shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
        wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        
        # Calculate elbow angle
        angle = self.calculate_angle(
            [shoulder.x, shoulder.y],
            [elbow.x, elbow.y],
            [wrist.x, wrist.y]
        )
        
        self.angle_buffer.append(angle)
        avg_angle = np.mean(list(self.angle_buffer)) if len(self.angle_buffer) > 0 else angle
        
        # Detect rep: arm goes down (angle < 90) and up (angle > 150)
        if avg_angle < 90:
            self.push_up_down = True
        elif avg_angle > 150 and self.push_up_down:
            self.push_up_counter += 1
            self.push_up_down = False
        
        return int(avg_angle)
    
    def detect_squat(self, landmarks):
        """Detect squat exercise"""
        # Get knee and hip joints
        hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        
        # Calculate knee angle
        angle = self.calculate_angle(
            [hip.x, hip.y],
            [knee.x, knee.y],
            [ankle.x, ankle.y]
        )
        
        self.angle_buffer.append(angle)
        avg_angle = np.mean(list(self.angle_buffer)) if len(self.angle_buffer) > 0 else angle
        
        # Detect rep: knee bends (angle < 90) and extends (angle > 160)
        if avg_angle < 90:
            self.squat_down = True
        elif avg_angle > 160 and self.squat_down:
            self.squat_counter += 1
            self.squat_down = False
        
        return int(avg_angle)
    
    def detect_plank(self, landmarks):
        """Detect plank position and track duration"""
        # Get shoulders and hips to check plank position
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        
        # Check if body is in plank position (horizontal)
        shoulder_y = left_shoulder.y
        hip_y = left_hip.y
        
        # If shoulder and hip are at similar height, it's plank position
        if abs(shoulder_y - hip_y) < 0.1:
            if not self.plank_started:
                self.plank_started = True
                self.start_time = time.time()
            self.plank_time = int(time.time() - self.start_time)
        else:
            self.plank_started = False
            self.start_time = None
        
        return self.plank_time
    
    def draw_stats(self, frame, exercise_type="demo"):
        """Draw exercise statistics on frame"""
        h, w = frame.shape[:2]
        
        # Background for stats
        cv2.rectangle(frame, (10, 10), (400, 150), (0, 0, 0), -1)
        cv2.rectangle(frame, (10, 10), (400, 150), (0, 255, 0), 2)
        
        # Display stats based on selected exercise
        if exercise_type == "pushup":
            cv2.putText(frame, "Exercise: Push-ups", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Reps: {self.push_up_counter}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
            cv2.putText(frame, "Press Q to quit", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 1)
        
        elif exercise_type == "squat":
            cv2.putText(frame, "Exercise: Squats", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Reps: {self.squat_counter}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
            cv2.putText(frame, "Press Q to quit", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 1)
        
        elif exercise_type == "plank":
            cv2.putText(frame, "Exercise: Plank", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Duration: {self.plank_time}s", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
            cv2.putText(frame, "Press Q to quit", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 1)
        
        else:  # Demo/pose detection mode
            cv2.putText(frame, "AI Gym Trainer - Demo Mode", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, "1: Push-ups | 2: Squats | 3: Plank", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 1)
            cv2.putText(frame, "Q: Quit", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 1)

def main():
    try:
        print("🏋️ Starting AI Gym Trainer...")
        
        cap = cv2.VideoCapture(0)
        
        # Check if camera opened successfully
        if not cap.isOpened():
            print("❌ Error: Could not open webcam. Please check:")
            print("   1. Camera is connected and not in use")
            print("   2. Camera permissions are granted")
            print("   3. Try restarting the application")
            input("Press Enter to close...")
            return
        
        print("✅ Camera opened successfully")
        
        detector = ExerciseDetector()
        current_exercise = "demo"
        
        # Get camera properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        print("✅ Loading MediaPipe Pose Detection...")
        
        with mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as pose:
            
            print("✅ MediaPipe loaded successfully!")
            print("\n🎯 Controls:")
            print("   1: Push-ups  |  2: Squats  |  3: Plank  |  Q: Quit\n")
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    print("Failed to grab frame")
                    break
                
                # Flip horizontally for selfie view
                frame = cv2.flip(frame, 1)
                h, w, c = frame.shape
                
                # Convert to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(image)
                
                # Convert back to BGR for OpenCV
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                
                # Draw pose landmarks
                if results.pose_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        results.pose_landmarks,
                        mp_pose.POSE_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                        mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
                    )
                    
                    # Get landmarks
                    landmarks = results.pose_landmarks.landmark
                    
                    # Process based on selected exercise
                    if current_exercise == "pushup":
                        detector.detect_push_up(landmarks)
                    elif current_exercise == "squat":
                        detector.detect_squat(landmarks)
                    elif current_exercise == "plank":
                        detector.detect_plank(landmarks)
                
                # Draw statistics
                detector.draw_stats(image, current_exercise)
                
                # Display instructions
                cv2.putText(image, "Press 1: Push-ups | 2: Squats | 3: Plank | Q: Quit", 
                           (10, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)
                
                cv2.imshow("🏋️ AI Gym Trainer - HealthHub", image)
                
                # Keyboard controls
                key = cv2.waitKey(10) & 0xFF
                if key == ord('q') or key == ord('Q'):
                    print("\n✅ Session ended")
                    break
                elif key == ord('1'):
                    print("💪 Push-ups mode activated")
                    current_exercise = "pushup"
                    detector.push_up_counter = 0
                elif key == ord('2'):
                    print("🦵 Squats mode activated")
                    current_exercise = "squat"
                    detector.squat_counter = 0
                elif key == ord('3'):
                    print("📍 Plank mode activated")
                    current_exercise = "plank"
                    detector.plank_time = 0
        
        cap.release()
        cv2.destroyAllWindows()
        print(f"\n📊 Final Stats:")
        print(f"   Push-ups: {detector.push_up_counter}")
        print(f"   Squats: {detector.squat_counter}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        input("Press Enter to close...")

if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
