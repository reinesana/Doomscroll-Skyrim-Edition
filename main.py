import cv2  
import mediapipe as mp  
import time
import subprocess
import os
from pathlib import Path

# On Windows, we use os.startfile to open and taskkill to close
def play_video(video_path: Path) -> None:
    os.startfile(str(video_path))

def close_video() -> None:
    # List of popular video players
    video_players = [
        "Video.UI.exe",      # Windows Movies & TV
        "vlc.exe",           # VLC
        "wmplayer.exe",      # Windows Media Player
        "mpv.exe",           # mpv
        "mpc-hc.exe",        # Media Player Classic
        "mpc-hc64.exe",      # Media Player Classic 64 bits
        "potplayer.exe",     # PotPlayer
        "ffplay.exe",        # FFPlay
    ]
    
    for player in video_players:
        subprocess.run(["taskkill", "/F", "/IM", player], 
                       stdout=subprocess.DEVNULL, 
                       stderr=subprocess.DEVNULL, 
                       check=False)

def draw_warning(frame, text="lock in twin"):
    h, w = frame.shape[:2]
    box_w, box_h = 500, 70
    x1 = (w - box_w) // 2
    y1 = 24
    x2 = x1 + box_w
    y2 = y1 + box_h

    overlay = frame.copy()
    cv2.rectangle(overlay, (x1, y1), (x2, y2), (15, 0, 15), -1)
    cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)
    cv2.rectangle(frame, (x1-2, y1-2), (x2+2, y2+2), (80, 255, 160) , 4)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (80, 255, 160) , 2)

    cv2.putText(
        frame,
        text.upper(),
        (x1 + 26, y1 + 48),
        cv2.FONT_HERSHEY_DUPLEX,
        1.2,
        (255, 255, 255),
        3,
        cv2.LINE_AA,
    )

def main():
    timer = 2.0
    looking_down_threshold = 0.25
    debounce_threshold = 0.45
    
    # Make sure this folder/file exists on your PC
    skyrim_skeleton_video = Path("./assets/skyrim-skeleton.mp4").resolve()
    if not skyrim_skeleton_video.exists():
        print(f"Video not found at: {skyrim_skeleton_video}")
        return
    
    face_mesh_landmarks = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Webcam could not be opened")
        return
    
    doomscroll = None
    video_playing = False

    while True:
        ret, frame = cam.read()
        if not ret:
            continue
        
        frame = cv2.flip(frame, 1)
        height, width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        processed_image = face_mesh_landmarks.process(rgb_frame)
        face_landmark_points = processed_image.multi_face_landmarks

        current = time.time()

        if face_landmark_points:
            one_face_landmark_points = face_landmark_points[0].landmark
            
            # Eye positions for the rectangle (aesthetic)
            left = [one_face_landmark_points[145], one_face_landmark_points[159]]
            right = [one_face_landmark_points[374], one_face_landmark_points[386]]
            
            lx = int((left[0].x + left[1].x) / 2 * width)
            ly = int((left[0].y + left[1].y) / 2 * height)
            rx = int((right[0].x + right[1].x) / 2 * width)
            ry = int((right[0].y + right[1].y) / 2 * height)

            box = 50
            cv2.rectangle(frame, (lx - box, ly - box), (lx + box, ly + box), (10, 255, 0), 2)
            cv2.rectangle(frame, (rx - box, ry - box), (rx + box, ry + box), (10, 255, 0), 2)
            
            l_iris = one_face_landmark_points[468]
            r_iris = one_face_landmark_points[473]
            
            l_ratio = (l_iris.y - left[1].y) / (left[0].y - left[1].y + 1e-6)
            r_ratio = (r_iris.y - right[1].y) / (right[0].y - right[1].y + 1e-6)

            avg_ratio = (l_ratio + r_ratio) / 2.0

            if video_playing:
                is_looking_down = avg_ratio < debounce_threshold
            else:
                is_looking_down = avg_ratio < looking_down_threshold

            if is_looking_down:
                if doomscroll is None:
                    doomscroll = current

                if (current - doomscroll) >= timer:                
                    if not video_playing:
                        play_video(skyrim_skeleton_video)
                        video_playing = True
            else:
                doomscroll = None
                if video_playing:
                    close_video()
                    video_playing = False
        else:
            doomscroll = None
            if video_playing:
                close_video()
                video_playing = False

        if video_playing:
            draw_warning(frame, "doomscrolling alarm")

        cv2.imshow('lock in', frame)
        if cv2.waitKey(1) == 27: # ESC to exit
            break

    if video_playing:
        close_video()

    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()