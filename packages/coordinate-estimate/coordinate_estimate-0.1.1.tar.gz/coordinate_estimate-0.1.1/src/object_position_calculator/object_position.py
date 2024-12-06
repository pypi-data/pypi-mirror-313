import socketio
import cv2
import numpy as np
import base64
import os
from datetime import datetime
from PIL import Image
import io
from ultralytics import YOLO
from detect_object import YOLOTracker
from newCalculator import newCoordinateCalculator


class DroneYOLOClient:
    def __init__(self, server_url, model_path):
        self.server_url = server_url
        self.sio = socketio.Client()
        self.lat, self.lng, self.heading, self.altitude = None, None, None, None
        self.pitch, self.fov_h, self.fov_v = None, None, None
        self._setup_event_handlers()
        self.model_path = model_path

    def _setup_event_handlers(self):
        @self.sio.event
        def connect():
            print("Connected to server!")
            room = "drone"
            self.sio.emit("join", {"room": room})
            print(f"Joined room: {room}")

        @self.sio.event
        def disconnect():
            print("Disconnected from server!")

        @self.sio.on("response_geo_drone")
        def on_geo_data(data):
            self.lat = data.get("lat")
            self.lng = data.get("lng")
            self.heading = data.get("heading")
            self.altitude = data.get("altitude")
            self.pitch = data.get("pitch")
            self.fov_v = data.get("fov_vertical")
            self.fov_h = data.get("fov_horizontal")
            print(f"[Drone] Received geo data: {data}")

        @self.sio.on("captured_image")
        def on_captured_image(data):
            image_byte_array = data.get("image_byte_array")
            if not image_byte_array:
                print("Error: No image byte array received.")
                return

            self._process_and_send_image(image_byte_array)

    def connect(self):
        try:
            self.sio.connect(self.server_url)
            print(f"Connected to {self.server_url}")
        except Exception as e:
            print(f"Failed to connect: {e}")

    def send_message_to_server(self, message="test message from YOLO"):
        room = "drone"
        self.sio.emit("response_from_yolo", {"room": room, "message": message})
        print("Sent message to server.")

    def send_drone_command(self, command, params=""):
        room = "drone"
        self.sio.emit("send_command", {
            "room": room, "command": command, "params": params, "requester": "yolo"
        })
        print("Sent drone command.")

    def _process_and_send_image(self, image_byte_array):
        save_folder = 'received_images'
        os.makedirs(save_folder, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        image_filename = os.path.join(save_folder, f'image_{timestamp}.png')

        image = Image.open(io.BytesIO(image_byte_array))
        image.save(image_filename)
        print(f"Image saved to {image_filename}")

        tracker = YOLOTracker(self.model_path)
        detections = tracker.process_image(image_filename)
        print(f"Detections: {detections}")

        image = cv2.imread(image_filename)
        for detected in detections:
            x, y = detected
            image_height, image_width = image.shape[:2]

            width, height = 50, 50
            top_left = (x - width // 2, y - height // 2)
            bottom_right = (x + width // 2, y + height // 2)
            cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

            calculator = newCoordinateCalculator(
                angle=self.pitch, height=self.altitude, gps_lat=self.lat,
                gps_lon=self.lng, image_width=image_width,
                image_height=image_height, detected_x=x, detected_y=y,
                fov=self.fov_v, bearing=self.heading
            )

            results = calculator.calculate_coordinates()
            print(f"Calculation Results: {results}")

        save_detection_folder = 'detected_images'
        os.makedirs(save_detection_folder, exist_ok=True)
        detected_image_filename = os.path.join(
            save_detection_folder, f'detected_image_{timestamp}.png'
        )
        cv2.imwrite(detected_image_filename, image)
        print(f"Processed image saved to {detected_image_filename}")

        # Send the image back to the server
        success, encoded_image = cv2.imencode('.png', image)
        if success:
            image_bytes = encoded_image.tobytes()
            room = "drone"
            self.sio.emit('send_image', {
                'room': room, 'image_byte_array': image_bytes, "requester": "webapp"
            })
            print("Sent processed image")
        else:
            print("Error encoding image.")

    def wait(self):
        self.sio.wait()


# Example usage:
if __name__ == "__main__":
    client = DroneYOLOClient("http://10.109.68.49:8000", "best.pt")
    client.connect()
    client.send_message_to_server("Hello, world from YOLO!")
    client.send_drone_command("capture_img")
    client.wait()
