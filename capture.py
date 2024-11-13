import os
import cv2
import csv
from clicker import get_arena
from constants import *
import time

def create_csv(folder_out, name):
    path = os.path.join(folder_out, f"{name}.csv")
    with open(path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["FrameID", "Time"])

def write_to_csv(folder_out, name, frame_i):
    path = os.path.join(folder_out, f"{name}.csv")
    with open(path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([frame_i, time.time()])

def check_name(name):
    forbidden_characters = [" ", ".", ",", "-"]
    for c in forbidden_characters:
        assert c not in name, f"Please remove '{c}' from the filename"

def main(folder_out: str, experiment_name: str):
    check_name(experiment_name)
    if not os.path.exists(folder_out):
        os.mkdir(folder_out)

    create_csv(folder_out, experiment_name)
    M = get_arena()
    
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()

    # Read the first frame from the video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 30
    size_old = (int(cap.get(3)), int(cap.get(4)))
    size_new = (frame_width, frame_height)
    
    writer = cv2.VideoWriter(os.path.join(folder_out, f'{experiment_name}.mp4'), fourcc, fps, size_new)
    cv2.namedWindow('Video recording')
    cv2.moveWindow('Video recording', 0, 0)
    
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        cap.release()
        exit()
        
    
    put_text_info = lambda frame_name, text: cv2.putText(frame_name.copy(), text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    frame_i = 0
    while True:
        # Display the frame
        ret, frame = cap.read()
        if not ret: break
        frame = cv2.warpPerspective(frame, M, size_old)[y0-B:y1+B, x0-B:x1+B, :]
        writer.write(frame)
        if frame_i % (5 * fps) == 0:
            write_to_csv(folder_out, experiment_name, frame_i)
        cv2.imshow('Video recording', put_text_info(frame, "q - end recording"))
    
        frame_i += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    writer.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    folder_out = "data"
    name = "test"
    main(folder_out, name)
    
    