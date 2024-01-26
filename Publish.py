# Import necessary libraries
import cv2
import numpy as np
import paho.mqtt.client as mqtt
import time
import threading

# MQTT broker details
MQTT_BROKER = "mqtt.eclipseprojects.io"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/webcam"

# Video capture object (replace 0 with the path to your video file if you want to read from a file)
cap = cv2.VideoCapture(0)

# MQTT client setup
client = mqtt.Client()

def publish_video_frames():
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Resize the frame to a smaller size (adjust dimensions as needed)
        resized_frame = cv2.resize(frame, (640, 480))

        # Reduce JPEG quality to 50 (adjust as needed)
        _, buffer = cv2.imencode('.jpg', resized_frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
        frame_bytes = buffer.tobytes()

        print("Publishing frame...")
        client.publish(MQTT_TOPIC, payload=frame_bytes, qos=0)

        time.sleep(0.1)


def on_message(client, userdata, message):
    frame_bytes = message.payload
    frame = cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), cv2.IMREAD_COLOR)
    cv2.imwrite('received_frame.jpg', frame)
    print(f"Frame received and saved. Shape: {frame.shape}")

# Set the callback function for MQTT messages
client.on_message = on_message

# Connect to the MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)
print("Connected to MQTT broker")

# Subscribe to the MQTT topic for receiving webcam frames
client.subscribe(MQTT_TOPIC)
print(f"Subscribed to MQTT topic: {MQTT_TOPIC}")

# Start the MQTT client loop in a separate thread
client.loop_start()

# Start the thread for publishing video frames to MQTT
publish_thread = threading.Thread(target=publish_video_frames)
publish_thread.start()

# Loop to handle video playback and exit on key press
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources and close windows
cap.release()
cv2.destroyAllWindows()

