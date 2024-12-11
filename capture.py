import os
import cv2
import csv
from datetime import datetime
from clicker import get_arena
from constants import *

def create_csv(folder_out, name):
    path = os.path.join(folder_out, f"{name}.csv")
    with open(path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["FrameID", "Time"])

def write_to_csv(csv_path, frame_i):
    current_time = datetime.now().strftime('%Y%m%d%H%M%S%f')
    with open(csv_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([frame_i, current_time])

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
    
    cap = cv2.VideoCapture(0, CAPTURE_MODE)
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
    csv_path = os.path.join(folder_out, f"{experiment_name}.csv")
    start_time = datetime.now()
    while True:
        # Display the frame
        ret, frame = cap.read()
        if not ret: break
        frame = cv2.warpPerspective(frame, M, size_old)
        frame = cv2.copyMakeBorder(
                frame,
                top=PAD,
                bottom=PAD,
                left=PAD,
                right=PAD,
                borderType=cv2.BORDER_CONSTANT,
                value=(0, 0, 0)  # Black padding
            )
        frame = frame[PAD:PAD+S+2*B, PAD:PAD+S+2*B, :]
        writer.write(frame)
        if frame_i % (5 * fps) == 0:
            write_to_csv(csv_path, frame_i)
        current_time = datetime.now()
        elapsed_time = current_time - start_time
        formatted_time = str(elapsed_time).split('.')[0]  # Remove microseconds
        cv2.imshow('Video recording', put_text_info(frame, f"q - end recording | {formatted_time}"))
    
        frame_i += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    write_to_csv(csv_path, frame_i)
    cap.release()
    writer.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    folder_out = "data"
    name = "test"
    main(folder_out, name)
    
    