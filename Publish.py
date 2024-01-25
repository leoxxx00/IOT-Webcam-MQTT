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

# Video capture object
cap = cv2.VideoCapture(0)

# MQTT client setup
client = mqtt.Client()

# Function to publish webcam frames to MQTT
def publish_webcam_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break

        # Encode the frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Publish the frame to the MQTT topic
        client.publish(MQTT_TOPIC, payload=frame_bytes, qos=0)

        # Wait for a short time (adjust as needed based on your application)
        time.sleep(0.1)

# Function to handle MQTT messages (subscribe)
def on_message(client, userdata, message):
    # Retrieve the frame bytes from the MQTT message payload
    frame_bytes = message.payload

    # Decode the frame and save it to a file (you can customize this part based on your application)
    frame = cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), cv2.IMREAD_COLOR)
    cv2.imwrite('received_frame.jpg', frame)

# Set the callback function for MQTT messages
client.on_message = on_message

# Connect to the MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Subscribe to the MQTT topic for receiving webcam frames
client.subscribe(MQTT_TOPIC)

# Start the MQTT client loop in a separate thread
client.loop_start()

# Start the thread for publishing webcam frames to MQTT
publish_thread = threading.Thread(target=publish_webcam_frames)
publish_thread.start()

# Wait for the user to press a key to exit
cv2.waitKey(0)

# Release resources and close windows
cap.release()
cv2.destroyAllWindows()
