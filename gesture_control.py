import cv2
import mediapipe as mp
import subprocess
import time
from gestures import GESTURE_COMMANDS

class GestureRecognizer:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.8
        )
        
        self.last_gesture = None
        self.last_time = 0
        self.cooldown = 3
    
    def get_fingers(self, landmarks):
        """Returns list of which fingers are up [thumb, index, middle, ring, pinky]"""
        fingers = []
        tips = [4, 8, 12, 16, 20]
        
        fingers.append(1 if landmarks[4].x > landmarks[3].x else 0)
        
        for i in range(1, 5):
            fingers.append(1 if landmarks[tips[i]].y < landmarks[tips[i] - 2].y else 0)
        
        return fingers
    
    def run_command(self, cmd):
        print(f"Running: {cmd}")
        try:
            subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            print(f"Error: {e}")
    
    def should_execute(self, gesture):
        now = time.time()
        if self.last_gesture != gesture or now - self.last_time > self.cooldown:
            self.last_gesture = gesture
            self.last_time = now
            return True
        return False
    
    def start(self):
        cap = cv2.VideoCapture(0)
        print("'q' to quit")        
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    fingers = self.get_fingers(hand_landmarks.landmark)
                    
                    for gesture_name, (command, pattern) in GESTURE_COMMANDS.items():
                        if fingers == pattern:
                            if self.should_execute(gesture_name):
                                self.run_command(command)
                    
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    
                    cv2.putText(frame, f"Fingers: {fingers}", (10, 30), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow("Hand Gestures", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    recognizer = GestureRecognizer()
    try:
        recognizer.start()
    except KeyboardInterrupt:
        print("\nBye!")