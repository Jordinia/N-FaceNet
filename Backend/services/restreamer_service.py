import cv2
from mjpeg_streamer import MjpegServer, Stream

def restreamer(cam_id: int, cam_url: str):
    """
    Starts the restreamer with the given camera URL and port.

    Parameters:
        cam_url (str): The URL of the video stream.
        port (int): The port number for the MJPEG server.
    """
    # Initialize video capture from the specified URL
    cap = cv2.VideoCapture(cam_url)

    # Initialize the MJPEG stream
    stream = Stream("camera", size=(640, 480), quality=50, fps=30)
    port=int(16000+cam_id)
    # Initialize and start the MJPEG server
    server = MjpegServer("0.0.0.0", port)
    server.add_stream(stream)
    server.start()

    print("--------------------------------")
    print("\nPress Ctrl+C to stop the server")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Ensure the frame is valid before displaying and streaming
        if frame is not None and frame.size > 0:
            stream.set_frame(frame)


    # Stop the server and release resources
    server.stop()
    cap.release()