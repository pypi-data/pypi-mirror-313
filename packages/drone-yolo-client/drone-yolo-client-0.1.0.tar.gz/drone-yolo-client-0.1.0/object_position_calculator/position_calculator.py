import math

class ObjectPositionCalculator:
    def __init__(self, focal_length=1000, earth_radius=6371):
        """
        Initialize the ObjectPositionCalculator with default constants.

        :param focal_length: The focal length of the camera in pixels.
        :param earth_radius: The radius of the Earth in kilometers.
        """
        self.focal_length = focal_length
        self.earth_radius = earth_radius

    def calculate_object_position(self, latitude, longitude, altitude, w, h):
        """
        Calculate the geographical position of an object.

        :param latitude: Latitude of the camera in degrees.
        :param longitude: Longitude of the camera in degrees.
        :param altitude: Altitude of the camera in kilometers.
        :param w: Width of the detected object in pixels.
        :param h: Height of the detected object in pixels (not used currently).
        :return: (latitude, longitude) of the object in degrees.
        """
        distance_to_object = (w * altitude) / self.focal_length

        # Calculate delta latitude and delta longitude
        delta_lat = distance_to_object / self.earth_radius
        delta_lon = distance_to_object / (self.earth_radius * math.cos(math.radians(latitude)))

        # Calculate object position
        lat_object = latitude + math.degrees(delta_lat)
        lon_object = longitude + math.degrees(delta_lon)

        return lat_object, lon_object

    def get_object_position(self, current_frame_detections, latitude, longitude, altitude, x, y, w, h):
        """
        Wrapper to calculate object position only if detections exist.

        :param current_frame_detections: Boolean indicating whether objects are detected.
        :param latitude: Latitude of the camera in degrees.
        :param longitude: Longitude of the camera in degrees.
        :param altitude: Altitude of the camera in kilometers.
        :param x, y: Coordinates of the object in the frame (not used).
        :param w: Width of the detected object in pixels.
        :param h: Height of the detected object in pixels (not used currently).
        :return: (latitude, longitude) of the object or (None, None) if no detections.
        """
        if current_frame_detections:
            return self.calculate_object_position(latitude, longitude, altitude, w, h)
        return None, None
if __name__ == "__main__":
    # Initialize the position calculator
    calculator = ObjectPositionCalculator(focal_length=1200, earth_radius=6371)

    # Simulated inputs
    current_frame_detections = True  # Assume objects were detected
    latitude = 37.7749  # San Francisco latitude
    longitude = -122.4194  # San Francisco longitude
    altitude = 0.1  # Drone altitude in kilometers (100 meters)
    x, y = 500, 300  # Object's position in the frame (not used)
    object_width = 50  # Object width in pixels
    object_height = 100  # Object height in pixels (not used currently)

    # Calculate object position
    object_position = calculator.get_object_position(
        current_frame_detections, latitude, longitude, altitude, x, y, object_width, object_height
    )

    # Output
    if object_position != (None, None):
        print("Detected Object Position (Latitude, Longitude):", object_position)
    else:
        print("No object detected in the frame.")