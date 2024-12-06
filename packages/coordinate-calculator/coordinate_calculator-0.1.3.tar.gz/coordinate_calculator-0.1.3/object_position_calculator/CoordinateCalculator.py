import math

class CoordinateCalculator2:
    def __init__(self, angle, bearing, height, gps_x, gps_y, fov, image_width, image_height, detected_x, detected_y):
        self.angle = angle
        self.bearing = bearing
        self.height = height
        self.gps_x = gps_x
        self.gps_y = gps_y
        self.fov = fov
        self.image_width = image_width
        self.image_height = image_height
        self.center_x = image_width / 2
        self.center_y = image_height / 2
        self.detected_x = detected_x
        self.detected_y = detected_y

    def calculate_principle_point_distance(self):
        """Calculate the principle point distance."""
        return self.height / math.cos(math.radians(self.angle))

    def calculate_distance_from_principle_point(self, principle_distance):
        """Calculate the distance from the principle point."""
        d_squared = principle_distance**2 - self.height**2
        return math.sqrt(d_squared)

    def convert_bearing_to_radians(self, bearing):
        """Convert bearing from degrees to radians."""
        return math.radians(bearing)

    def calculate_coordinate_change(self, distance, radian):
        """Calculate coordinate change Δx and Δy."""
        delta_x = distance * math.sin(radian)
        delta_y = distance * math.cos(radian)
        return delta_x, delta_y

    def calculate_new_coordinates(self, x_start, y_start, delta_x, delta_y):
        """Calculate new coordinates."""
        x_new = x_start + delta_x
        y_new = y_start + delta_y
        return x_new, y_new

    def pixels_to_meters(self, d_pixels):
        """Convert pixel distance to meters."""
        pixel_scale = (self.height * math.tan(math.radians(self.fov) / 2)) / (self.image_width / 2)
        return d_pixels * pixel_scale

    def calculate_bearing_offset(self, center_x, center_y, point_x, point_y):
        """Calculate bearing offset (Delta Bearing)."""
        delta_bearing_radians = math.atan2(center_y - point_y, point_x - center_x)
        delta_bearing_degrees = math.degrees(delta_bearing_radians)
        return delta_bearing_degrees

    def calculate(self):
        """Perform all calculations."""
        # Step 1-4: Calculate principle point distance and distance from principle point
        principle_distance = self.calculate_principle_point_distance()
        d_principle = self.calculate_distance_from_principle_point(principle_distance)

        # Step 5-7: Convert bearing to radians and calculate new coordinates of point P
        radian_bearing = self.convert_bearing_to_radians(self.bearing)
        delta_x, delta_y = self.calculate_coordinate_change(d_principle, radian_bearing)
        new_x, new_y = self.calculate_new_coordinates(self.gps_x, self.gps_y, delta_x, delta_y)
        print(new_x, new_y)

        # Step 8-10: Convert pixel distance to meters and calculate new bearing
        d_pixels = math.sqrt((self.detected_x - self.center_x)**2 + (self.detected_y - self.center_y)**2)
        d_meters = self.pixels_to_meters(d_pixels)
        delta_bearing = self.calculate_bearing_offset(self.center_x, self.center_y, self.detected_x, self.detected_y)

        # Step 11-13: Calculate new bearing and coordinates of point F
        new_bearing = (self.bearing + delta_bearing) % 360
        radian_new_bearing = self.convert_bearing_to_radians(new_bearing)
        delta_x_f, delta_y_f = self.calculate_coordinate_change(d_meters, radian_new_bearing)
        f_x, f_y = self.calculate_new_coordinates(self.gps_x, self.gps_y, delta_x_f, delta_y_f)

        # Output results
        return {
            "Ground Coordinates of G": (self.gps_x, self.gps_y),
            "New Coordinates of P": (new_x, new_y),
            "Distance in Pixels": d_pixels,
            "Distance in Meters": d_meters,
            "Delta Bearing": delta_bearing,
            "New Coordinates of F": (f_x, f_y)
        }

# Example Usage
calculator = CoordinateCalculator2(
    angle=90,
    bearing=7.575611114501953,
    height=25.0000057220459,
    gps_x=14.040890243218062,
    gps_y=100.61035146028303,
    fov=106.70455169677734,
    image_width=640,
    image_height=640,
    detected_x=100,
    detected_y=50
)

results = calculator.calculate()
for key, value in results.items():
    print(f"{key}: {value}")
