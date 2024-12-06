import math

class newCoordinateCalculator:
    def __init__(self, angle, height, gps_lat, gps_lon, image_width, image_height, detected_x, detected_y, fov,bearing):
        self.angle = angle
        self.height = height
        self.gps_lat = gps_lat
        self.gps_lon = gps_lon
        self.image_width = image_width
        self.image_height = image_height
        self.detected_x = detected_x
        self.detected_y = detected_y
        self.center_x = image_width / 2
        self.center_y = image_height / 2
        self.fov = fov 
        self.bearing = bearing,

    def calculate_principle_point_distance(self):
        """Calculate principle point distance."""
        return self.height / math.cos((math.radians(self.angle)))

    def calculate_distance(self, principle_distance):
        """Calculate horizontal distance from principle point."""
        return math.sqrt(principle_distance**2 - self.height**2)
    
    def haversine_distance(self, lat1, lon1, lat2, lon2):
        """Calculate Haversine distance between two latitude/longitude points."""
        R = 6371e3  # Earth's radius in meters
        d_lat = math.radians(lat2 - lat1) 
        d_lon = math.radians(lon2 - lon1)
        lat1 = math.radians(lat1)
        lat2 = math.radians(lat2)

        a = math.sin(d_lat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c
    
    def euclideain_distance(self,  lat_f, lng_f):
        """Calculate Haversine distance between two latitude/longitude points."""
        d_lat = (self.gps_lat - lat_f)**2
        d_lon = (self.gps_lon - lng_f)**2
        d = d_lat + d_lon + self.height**2
        return math.sqrt(d)

    def pixels_to_meters(self, d_pixels):
        """Convert pixel distance to meters."""
        # Calculate pixel-to-meter ratio based on FOV
        pixel_scale = (self.height * math.tan(math.radians(self.fov) / 2)) / (self.image_width / 2)
        return d_pixels * pixel_scale

    def calculate_bearing_offset(self, point_x, point_y):
        """Calculate bearing offset of a point."""
        delta_bearing_radians = math.atan2(self.center_y - point_y, point_x - self.center_x)
        return math.degrees(delta_bearing_radians)

    def haversine_new_coordinates(self, lat, lon, distance, bearing):
        """Calculate new latitude and longitude from a point using distance and bearing."""
        R = 6371e3  # Earth's radius in meters
        bearing = math.radians(self.bearing[0])

        lat = math.radians(lat)
        lon = math.radians(lon)

        new_lat = math.asin(math.sin(lat) * math.cos(distance / R) +
                            math.cos(lat) * math.sin(distance / R) * math.cos(bearing))
        new_lon = lon + math.atan2(math.sin(bearing) * math.sin(distance / R) * math.cos(lat),
                                   math.cos(distance / R) - math.sin(lat) * math.sin(new_lat))

        return math.degrees(new_lat), math.degrees(new_lon)

    def calculate_coordinates(self):
        """Main function to calculate all required distances and coordinates."""
        # Step 1: Calculate principle point distance
        principle_distance = self.calculate_principle_point_distance()

        # Step 2: Calculate horizontal distance d
        horizontal_distance = self.calculate_distance(principle_distance)

        # Step 3: Calculate P coordinates using Haversine formula
        lat_p, lon_p = self.haversine_new_coordinates(self.gps_lat, self.gps_lon, horizontal_distance, self.bearing)

        # Step 4: Convert pixel distance to meters
        d_pixels = math.sqrt((self.detected_x - self.center_x)**2 + (self.detected_y - self.center_y)**2)
        d_meters = self.pixels_to_meters(d_pixels)

        # Step 5: Calculate bearing offset
        bearing = self.calculate_bearing_offset(self.detected_x, self.detected_y)

        # Step 6: Calculate F coordinates
        lat_f, lon_f = self.haversine_new_coordinates(lat_p, lon_p, d_meters, bearing)

        # Step 7: Calculate distance between G and F
        distance_gf = self.haversine_distance(self.gps_lat, self.gps_lon, lat_f, lon_f)

        return {
            "principle_distance": principle_distance,
            "horizontal_distance": horizontal_distance,
            "coordinates_p": (lat_p, lon_p),
            "coordinates_f": (lat_f, lon_f),
            "distance_gf": distance_gf,
            "bearing_offset": bearing
        }

# Example values
calculator = newCoordinateCalculator(
    angle=30,                # มุมกล้อง
    height=100,              # ความสูงของกล้อง (เมตร)
    gps_lat=13.736717,       # ละติจูดจุด G
    gps_lon=100.523186,      # ลองจิจูดจุด G
    image_width=640,         # ความกว้างของภาพ
    image_height=640,        # ความสูงของภาพ
    detected_x=320,          # พิกัด X ของจุด F ในภาพ
    detected_y=200,          # พิกัด Y ของจุด F ในภาพ
    fov = 90,
    bearing = 15
)

results = calculator.calculate_coordinates()

# print("Calculation Results:")
# print(f"GPS Latitude, Longitude: {calculator.gps_lat}, {calculator.gps_lon}")
# print(f"1. Principle Distance (P): {results['principle_distance']:.2f} meters")
# print(f"2. Horizontal Distance (d): {results['horizontal_distance']:.2f} meters")
# print(f"3. Coordinates of Point P: Latitude {results['coordinates_p'][0]:.15f}, Longitude {results['coordinates_p'][1]:.15f}")
# print(f"4. Coordinates of Point F: Latitude {results['coordinates_f'][0]:.15f}, Longitude {results['coordinates_f'][1]:.15f}")
# print(f"5. Distance between G and F: {results['distance_gf']:.2f} meters")
# print(f"6. Bearing Offset to Point F: {results['bearing_offset']:.2f} degrees")
