import cv2
import mediapipe as mp
import math as m
import mouse

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

hands = mp.solutions.hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

lclicked = rclicked = False
prev_x = prev_y = fx = fy = None
smoothed_x = smoothed_y = 0
moveDir = [0, 0]
screen_w, screen_h = 1920, 1080
sensitivity = 3
smoothTime = 0.25
deadzone = 1

def lerp(a, b, t):
    return a + (b - a) * t

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for connection in mp.solutions.hands.HAND_CONNECTIONS:
                x1, y1 = int(hand_landmarks.landmark[connection[0]].x * w), int(hand_landmarks.landmark[connection[0]].y * h)
                x2, y2 = int(hand_landmarks.landmark[connection[1]].x * w), int(hand_landmarks.landmark[connection[1]].y * h)
                cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)
            
            for lm in hand_landmarks.landmark:
                cv2.circle(frame, (int(lm.x * w), int(lm.y * h)), 1, (255, 255, 255), 2)

            thumb = hand_landmarks.landmark[4]
            index = hand_landmarks.landmark[8]
            middle = hand_landmarks.landmark[12]
            control = hand_landmarks.landmark[0]

            tx, ty = int(thumb.x * w), int(thumb.y * h)
            ix, iy = int(index.x * w), int(index.y * h)
            mx, my = int(middle.x * w), int(middle.y * h)
            cx, cy = int(control.x * screen_w), int(control.y * screen_h)

            cv2.line(frame, (mx, my), (tx, ty), (0, 255, 255), 2)
            cv2.line(frame, (ix, iy), (tx, ty), (0, 255, 255), 2)

            thumb_index_dist = m.dist((tx, ty), (ix, iy))
            thumb_middle_dist = m.dist((tx, ty), (mx, my))

            clickThreshold = 25
            
            if thumb_index_dist <= clickThreshold:
                if not lclicked:
                    mouse.press("left")
                    lclicked = True
            elif lclicked:
                mouse.release("left")
                lclicked = False

            if thumb_middle_dist <= clickThreshold:
                if not rclicked:
                    mouse.press("right")
                    rclicked = True
            elif rclicked:
                mouse.release("right")
                rclicked = False

            smoothed_x = lerp(smoothed_x, cx, smoothTime)
            smoothed_y = lerp(smoothed_y, cy, smoothTime)
            
            if prev_x is not None and fx is not None:
                dx = (smoothed_x - prev_x) * sensitivity
                dy = (smoothed_y - prev_y) * sensitivity
                
                distance_from_start = m.sqrt((smoothed_x - fx)**2 + (smoothed_y - fy)**2)
                
                if distance_from_start > deadzone:
                    mouse.move(int(dx), int(dy), absolute=False)
            
            prev_x, prev_y = smoothed_x, smoothed_y
            if fx is None:
                fx, fy = smoothed_x, smoothed_y

    cv2.imshow("HandFlow", frame)
    key = cv2.waitKey(1) & 0xFF
    if cv2.getWindowProperty("HandFlow", cv2.WND_PROP_VISIBLE) < 1:
        break
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()