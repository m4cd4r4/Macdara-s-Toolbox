import cv2
import numpy as np
import pygetwindow as gw
import pyautogui

def record_screen(output_file='recording.avi', screen_area=None, fps=20.0, record_time=10):
    """
    Records a portion of the screen to a video file.

    Args:
    output_file (str): The filename to save the recording.
    screen_area (tuple): The area of the screen to record, in the format (x, y, width, height).
                        If None, records the entire screen.
    fps (float): Frames per second in the output video.
    record_time (int): Duration of the recording in seconds.
    """
    # Determine the screen area to record
    if screen_area is None:
        screen_area = (0, 0, pyautogui.size().width, pyautogui.size().height)

    x, y, width, height = screen_area

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    for _ in range(int(30 * 15)):
        # Take a screenshot
        img = pyautogui.screenshot(region=(x, y, width, height))

        # Convert the image to numpy array
        frame = np.array(img)

        # Convert the image from BGR to RGB (OpenCV uses BGR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Write the frame to the video file
        out.write(frame)

        # Wait for a while between screenshots
        cv2.waitKey(int(1000 / fps))

    # Release everything when done
    out.release()
    cv2.destroyAllWindows()

# Example usage
record_screen(output_file='my_screen_recording.avi', record_time=5)
