import math

class CoordinateCalculator:
    def __init__(self, angle_deg, bearing_deg, height, gps_lat, gps_lng, image_size, detected_x, detected_y, pixel_to_meter_ratio):
        self.angle_deg = angle_deg
        self.bearing_deg = bearing_deg
        self.height = height
        self.gps_lat = gps_lat
        self.gps_lng = gps_lng
        self.image_size = image_size
        self.detected_x = detected_x
        self.detected_y = detected_y
        self.pixel_to_meter_ratio = pixel_to_meter_ratio

    def calculate_principle_point(self):
        """Calculate the principle point using the formula: Height * sec(angle)"""
        angle_rad = math.radians(self.angle_deg)  # Convert angle to radians
        return self.height * (1 / math.cos(angle_rad))  # sec(angle) = 1 / cos(angle)

    def calculate_distance(self, principle_point):
        """Calculate the distance d using the formula: d^2 = (Principle Point)^2 - Height^2"""
        d_squared = (principle_point ** 2) - (self.height ** 2)
        return math.sqrt(d_squared)

    def convert_bearing_to_radians(self):
        """Convert the bearing angle from degrees to radians"""
        return math.radians(self.bearing_deg)

    def calculate_coordinate_changes(self, d, bearing_rad):
        """Calculate the change in coordinates (Δx, Δy) using: Δx = d * cos(radian), Δy = d * sin(radian)"""
        delta_x = d * math.cos(bearing_rad)
        delta_y = d * math.sin(bearing_rad)
        return delta_x, delta_y

    def calculate_new_coordinates(self, delta_x, delta_y):
        """Calculate the new coordinates (latitude, longitude) by adding changes to the start coordinates"""
        x_new = self.gps_lat + delta_x
        y_new = self.gps_lng + delta_y
        return x_new, y_new

    def calculate_image_center(self):
        """Calculate the center point (xc, yc) of an image with given width and height"""
        width, height = self.image_size
        xc = width / 2
        yc = height / 2
        return xc, yc

    def calculate_euclidean_distance(self, x1, y1, detected_x, detected_y):
        """Calculate the Euclidean distance between two points (x1, y1) and (detected_x, detected_y)"""
        return math.sqrt((detected_x - x1) ** 2 + (detected_y - y1) ** 2)

    def convert_distance_to_meters(self, distance_pixels):
        """Convert distance from pixels to meters using the formula: d(meters) = d(pixels) × X"""
        return distance_pixels * self.pixel_to_meter_ratio

    def calculate_bearing_from_center(self, xc, yc, x_f, y_f):
        """Calculate the bearing from the center (x_center, y_center) to the point F (x_f, y_f)"""
        delta_bearing = math.atan2(yc - y_f, x_f - xc)
        return math.degrees(delta_bearing)  # Return in degrees
    
    
    def main(self):
        # Step 1: Calculate Principle Point
        principle_point = self.calculate_principle_point()

        # Step 2: Calculate Distance
        d = self.calculate_distance(principle_point)

        # Step 3: Convert Bearing to Radians
        bearing_rad = self.convert_bearing_to_radians()

        # Step 4: Calculate Coordinate Changes (Δx, Δy)
        delta_x, delta_y = self.calculate_coordinate_changes(d, bearing_rad)

        # Step 5: Calculate New Coordinates
        x_new, y_new = self.calculate_new_coordinates(delta_x, delta_y)

        # Step 6: Calculate Euclidean Distance between new coordinates and detected point
        distance_pf_pixels = self.calculate_euclidean_distance(x_new, y_new, self.detected_x, self.detected_y)

        # Step 7: Convert Distance to Meters
        distance_pf_meters = self.convert_distance_to_meters(distance_pf_pixels)

        # Step 8: Calculate Bearing from the center of the image to the point (detected_x, detected_y)
        xc, yc = self.calculate_image_center()
        bearing_from_center = self.calculate_bearing_from_center(xc, yc, self.detected_x, self.detected_y)

        # Calculate the new position using the bearing from the image center
        bearing_center_rad = math.radians(bearing_from_center)
        f_x, f_y = self.calculate_coordinate_changes(distance_pf_meters, bearing_center_rad)
        xf_new, yf_new = self.calculate_new_coordinates(f_x, f_y)

        # Return results in a dictionary
        return {
            "Ground Coordinates of G": (self.gps_lat, self.gps_lng),
            "New Coordinates of P": (x_new, y_new),
            "Distance in Pixels": distance_pf_pixels,
            "Distance in Meters": distance_pf_meters,
            "Delta Bearing": bearing_from_center,
            "New Coordinates of F": (xf_new, yf_new)
        }

# Example usage
angle = 30  # in degrees
bearing = 45  # in degrees
height = 25  # in meters
gps_lat, gps_lng = 50, 100  # Example GPS coordinates
image_size = (640, 640)  # Example image size
detected_x, detected_y = 219.15426635742188, 439.4124755859375  # Detected point in the image
pixel_to_meter_ratio = 0.01  # Example ratio: 1 pixel = 0.01 meters

calculator = CoordinateCalculator(angle, bearing, height, gps_lat, gps_lng, image_size, detected_x, detected_y, pixel_to_meter_ratio)
results = calculator.main()

# Print results
# print(f"Ground Coordinates of G: {results['Ground Coordinates of G']}")
# print(f"New Coordinates of P: {results['New Coordinates of P']}")
# print(f"Distance in Pixels: {results['Distance in Pixels']:.2f} px")
# print(f"Distance in Meters: {results['Distance in Meters']:.2f} m")
# print(f"Bearing from Image Center: {results['Delta Bearing']:.2f} degrees")
# print(f"New Coordinates of F: {results['New Coordinates of F']}")