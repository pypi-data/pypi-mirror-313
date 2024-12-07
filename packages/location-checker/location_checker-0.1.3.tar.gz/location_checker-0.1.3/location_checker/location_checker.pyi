from typing import Optional, List


class Location:
    """
    Represents a geographical location with latitude, longitude, and an optional timestamp.

    Attributes:
        latitude (float): Latitude of the location, must be between -90 and 90.
        longitude (float): Longitude of the location, must be between -180 and 180.
        timestamp (Optional[datetime.datetime]): An optional RFC3339 formatted timestamp.
    """

    latitude: float
    longitude: float
    timestamp: Optional["datetime.datetime"]

    def __init__(self, latitude: float, longitude: float, timestamp: Optional[str] = None) -> None:
        """
        Initializes a new Location object.

        Args:
            latitude (float): Latitude of the location, must be between -90 and 90.
            longitude (float): Longitude of the location, must be between -180 and 180.
            timestamp (Optional[str]): An optional RFC3339 formatted timestamp.

        Raises:
            ValueError: If latitude, longitude, or timestamp are invalid.
        """
        ...


class LocationChecker:
    """
    Provides utilities for location-related operations such as country lookup, distance calculation,
    and travel time verification.
    """

    def __init__(self) -> None:
        """
        Initializes the LocationChecker and ensures boundaries are loaded.
        """
        ...

    @staticmethod
    def load_boundaries() -> None:
        """
        Loads country boundaries into memory. Must be called before performing any operations.

        Raises:
            ValueError: If boundaries fail to load.
        """
        ...

    def get_country(self, location: Location) -> List[str]:
        """
        Determines the country (or countries) for a given location.

        Args:
            location (Location): The location to check.

        Returns:
            List[str]: A list of country codes associated with the location.

        Raises:
            ValueError: If boundaries are not loaded or if location coordinates are invalid.
        """
        ...

    def calculate_distance(self, location1: Location, location2: Location) -> float:
        """
        Calculates the Haversine distance between two locations.

        Args:
            location1 (Location): The first location.
            location2 (Location): The second location.

        Returns:
            float: Distance between the locations in meters.
        """
        ...

    def verify_travel_time(self, start_location: Location, end_location: Location) -> bool:
        """
        Verifies whether travel between two locations within the given timestamps is feasible
        based on a realistic speed limit.

        Args:
            start_location (Location): The starting location with a timestamp.
            end_location (Location): The ending location with a timestamp.

        Returns:
            bool: True if travel is feasible, False otherwise.

        Raises:
            ValueError: If either location is missing a valid timestamp.
        """
        ...
