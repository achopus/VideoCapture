import cv2
import numpy as np

from constants import *

def get_arena():
    # Global variables to store points
    points = []
    reset_selection = False
    POINT_NAMES = ["Top left", "Top right", "Bottom right", "Bottom left"]
    POINT_COLORS = [(0, 0, 255), (255, 0, 0), (0, 255, 0), (125, 0, 125)]
    # Callback function to handle mouse events
    def select_points(event, x, y, flags, param):
        nonlocal points, reset_selection
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(points) < 4:  # Only allow 4 points
                points.append((x, y))
    
    put_text = lambda frame_name, point, i: cv2.putText(frame_name, POINT_NAMES[i], (point[0] + 10, point[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, POINT_COLORS[i], 2, cv2.LINE_AA)
    put_text_info = lambda frame_name, text: cv2.putText(frame_name,text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    
    def plot_text(frame, points):
        frame_copy = frame.copy()
        for i, point in enumerate(points):
            cv2.circle(frame_copy, point, radius=5, color=POINT_COLORS[i], thickness=-1)
            put_text(frame_copy, point, i)
        return frame_copy
    
    def plot_info_text(frame, is_transformed: bool):
        frame_copy = frame.copy()
        if is_transformed:
            text = "r - reset selection (long press) | q - finalize selection"
        else:
            text = "Left click = Select corner. Go clockwise, starting at 'Top Left' corner. | q - end selection (no transformation)"
        put_text_info(frame_copy, text)
        return frame_copy

    # Open video file or capture from camera
    cap = cv2.VideoCapture(0, CAPTURE_MODE)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()

    # Read the first frame from the video
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        cap.release()
        exit()
        
    size_old = (int(cap.get(3)), int(cap.get(4)))

    
    # Create a window and set mouse callback function
    cv2.namedWindow('Frame')
    cv2.moveWindow('Frame', 0, 0)
    #cv2.moveWindow('Frame', (1920 - 1600) // 2, (1080 - 900) // 2)
    #cv2.resizeWindow('Frame', 1600, 900)
    cv2.setWindowProperty('Frame', cv2.WND_PROP_TOPMOST, 1)
    cv2.setWindowProperty('Frame', cv2.WINDOW_NORMAL, 1)
    cv2.setMouseCallback('Frame', select_points)

    # Display the frame and wait for 4 points to be selected
    points_selected = False

    M = np.eye(3)
    while True:
        # Display the frame
        ret, frame = cap.read()
        if not ret: break
        
        if reset_selection:
            reset_selection = False
            points_selected = False
            points = []
        
        #cv2.namedWindow('Frame', cv2.WINDOW_FULLSCREEN)
        if points_selected:
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
            cv2.imshow('Frame', plot_info_text(frame, is_transformed=True))
            cv2.setWindowProperty('Frame', cv2.WINDOW_NORMAL, 1)
        else:
            cv2.imshow('Frame', plot_info_text(plot_text(frame, points), is_transformed=False))
            cv2.setWindowProperty('Frame', cv2.WINDOW_NORMAL, 1)
        
        # Check if 4 points have been selected
        if len(points) == 4 and not points_selected:
            points_selected = True
            corners = np.array(points)
            M = cv2.getPerspectiveTransform(np.float32(corners), np.float32(DEFINED_CORNERS))
            
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.waitKey(1) & 0xFF == ord('r'):
            points_selected = False
            points = []
        
        
    # Release the video capture and close windows
    cap.release()
    cv2.destroyAllWindows()
    return M

if __name__ == "__main__":
    get_arena()