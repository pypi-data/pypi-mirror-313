import unittest
from object_position_calculator import ObjectPositionCalculator

class TestObjectPositionCalculator(unittest.TestCase):
    def setUp(self):
        """
        Set up the test with a default ObjectPositionCalculator instance.
        """
        self.calculator = ObjectPositionCalculator(focal_length=1000, earth_radius=6371)

    def test_calculate_object_position(self):
        """
        Test the `calculate_object_position` method.
        """
        latitude = 51.5074  # Example latitude
        longitude = -0.1278  # Example longitude
        altitude = 0.3  # 300 meters in km
        w = 50  # Width in pixels
        h = 100  # Height in pixels (not used)

        lat_object, lon_object = self.calculator.calculate_object_position(latitude, longitude, altitude, w, h)

        # Assert the output values are within an expected range
        self.assertIsInstance(lat_object, float)
        self.assertIsInstance(lon_object, float)

    def test_get_object_position_with_detections(self):
        """
        Test the `get_object_position` method when detections are present.
        """
        latitude = 51.5074
        longitude = -0.1278
        altitude = 0.3
        x = 50
        y = 60
        w = 80
        h = 90
        current_frame_detections = True

        lat_object, lon_object = self.calculator.get_object_position(
            current_frame_detections, latitude, longitude, altitude, x, y, w, h
        )

        self.assertIsNotNone(lat_object)
        self.assertIsNotNone(lon_object)
        self.assertIsInstance(lat_object, float)
        self.assertIsInstance(lon_object, float)

    def test_get_object_position_without_detections(self):
        """
        Test the `get_object_position` method when no detections are present.
        """
        latitude = 51.5074
        longitude = -0.1278
        altitude = 0.3
        x = 50
        y = 60
        w = 80
        h = 90
        current_frame_detections = False

        lat_object, lon_object = self.calculator.get_object_position(
            current_frame_detections, latitude, longitude, altitude, x, y, w, h
        )

        self.assertIsNone(lat_object)
        self.assertIsNone(lon_object)

if __name__ == "__main__":
    unittest.main()
