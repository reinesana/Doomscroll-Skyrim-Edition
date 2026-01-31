import cv2
import mediapipe as mp
import time
import subprocess
from pathlib import Path

BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode


def osascript(script: str) -> None:
    subprocess.run(
        ["osascript", "-e", script],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )

def play_video(video_path: Path) -> None:
    absolute_path = str(video_path)
    script = f'''
    tell application "QuickTime Player"
        activate
        set doc to open POSIX file "{absolute_path}"

        tell doc
            play
            set presenting to false
            tell front window
                set bounds to {25, 45, 415, 825}
            end tell

        end tell
    end tell
    '''
    osascript(script)


def close_video(video_path: Path) -> None:
    video_name = video_path.name
    script = f'''
    tell application "QuickTime Player"
        repeat with d in documents
            try
                if (name of d) is "{video_name}" then
                    stop d
                    close d saving no
                end if
            end try
        end repeat
    end tell
    '''
    osascript(script)

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
    start_threshold = 0.4
    maintain_threshold = 0.3

    skyrim_skeleton_video = Path("./assets/skyrim-skeleton.mp4").resolve()
    if not skyrim_skeleton_video.exists():
        print("Could not open skyrim-skeleton.mp4")
        return

    model_path = Path("./assets/face_landmarker.task").resolve()
    if not model_path.exists():
        print("Missing model. Run: curl -o assets/face_landmarker.task https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task")
        return

    options = FaceLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=str(model_path)),
        running_mode=VisionRunningMode.VIDEO,
        output_face_blendshapes=True,
        num_faces=1)

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Could not open webcam")
        return

    fps = cam.get(cv2.CAP_PROP_FPS) or 30
    frame_timestamp_ms = 0

    doomscroll = None
    video_playing = False
    not_looking_count = 0
    reset_threshold = 10

    with FaceLandmarker.create_from_options(options) as landmarker:
        while True:
            ret, frame = cam.read()
            if not ret:
                continue

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            result = landmarker.detect_for_video(mp_image, int(frame_timestamp_ms))
            frame_timestamp_ms += 1000 / fps
            face_landmark_points = result.face_landmarks

            current = time.time()

            blendshapes = result.face_blendshapes

            if blendshapes and len(blendshapes[0]) > 12:
                bs = blendshapes[0]
                look_down_score = (bs[11].score + bs[12].score) / 2.0

                threshold = maintain_threshold if video_playing else start_threshold
                is_looking_down = look_down_score > threshold

                if is_looking_down:
                    not_looking_count = 0
                    if doomscroll is None:
                        doomscroll = current

                    if (current - doomscroll) >= timer:
                        if not video_playing:
                            play_video(skyrim_skeleton_video)
                            video_playing = True

                else:
                    not_looking_count += 1
                    if not_looking_count >= reset_threshold:
                        doomscroll = None
                        if video_playing:
                            close_video(skyrim_skeleton_video)
                            video_playing = False
            else:
                not_looking_count += 1
                if not_looking_count >= reset_threshold:
                    doomscroll = None
                    if video_playing:
                        close_video(skyrim_skeleton_video)
                        video_playing = False

            if video_playing:
                draw_warning(frame, "doomscrolling alarm")

            cv2.imshow('lock in', frame)
            key = cv2.waitKey(1)

            if key == 27:
                break

        if video_playing:
            close_video(skyrim_skeleton_video)

    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
