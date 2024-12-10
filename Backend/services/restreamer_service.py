import cv2
from mjpeg_streamer import MjpegServer, Stream

def restreamer(cam_id: int, cam_url: str):
    """
    Starts the restreamer with the given camera URL and port.

    Parameters:
        cam_id (int): The ID of the camera.
        cam_url (str): The URL of the video stream.
    """
    # Initialize video capture from the specified URL
    cap = cv2.VideoCapture(cam_url)
    if not cap.isOpened():
        print(f"Error: Could not open video stream from URL: {cam_url}")
        return

    # Initialize the MJPEG stream
    stream = Stream("camera", size=(640, 480), quality=50, fps=30)
    port = int(16000 + cam_id)

    # Initialize and start the MJPEG server
    server = MjpegServer("0.0.0.0", port)
    server.add_stream(stream)
    server.start()

    print(f"Streams index: http://localhost:{port}")
    print("Available streams:")
    print(f"http://localhost:{port}/camera")
    print("--------------------------------")
    print("\nPress Ctrl+C to stop the server")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            # Ensure the frame is valid before displaying and streaming
            if frame is not None and frame.size > 0:
                stream.set_frame(frame)
    except KeyboardInterrupt:
        print("Stopping...")

    # Stop the server and release resources
    server.stop()
    cap.release()

# # TESTING
# if __name__ == "__main__":
#     cam_id = 1
#     # cam_url = "http://100.79.3.2:1945/"  # Ensure this URL is correct
#     cam_url = "rtsp://100.111.29.103:1945/"  # Ensure this URL is correct
#     restreamer(cam_id, cam_url)