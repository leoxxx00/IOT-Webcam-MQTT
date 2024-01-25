# Import necessary libraries
import cv2
import numpy as np
import paho.mqtt.client as mqtt

# MQTT broker details
MQTT_BROKER = "mqtt.eclipseprojects.io"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/webcam"

# Video display window
cv2.namedWindow("Webcam Feed", cv2.WINDOW_NORMAL)

# MQTT client setup
client = mqtt.Client()

# Function to handle MQTT messages (subscribe)
def on_message(client, userdata, message):
    # Retrieve the frame bytes from the MQTT message payload
    frame_bytes = message.payload

    # Decode the frame and display it
    frame = cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), cv2.IMREAD_COLOR)
    cv2.imshow('Webcam Feed', frame)
    cv2.waitKey(1)  # Refresh window

# Set the callback function for MQTT messages
client.on_message = on_message

# Connect to the MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Subscribe to the MQTT topic for receiving webcam frames
client.subscribe(MQTT_TOPIC)

# Start the MQTT client loop
client.loop_forever()
