from location_checker import Location, LocationChecker


def test_location_checker():
    checker = LocationChecker()

    # Load boundaries
    checker.load_boundaries()

    # Test location creation
    loc1 = Location(latitude=37.7749, longitude=-122.4194, timestamp="2024-12-01T10:00:00Z")
    loc2 = Location(latitude=34.0522, longitude=-118.2437, timestamp="2024-12-01T14:00:00Z")

    # Test country lookup
    countries = checker.get_country(loc1)
    assert len(countries) > 0, "Country lookup failed"

    # Test distance calculation
    distance = checker.calculate_distance(loc1, loc2)
    assert distance > 0, "Distance calculation failed"

    # Test travel feasibility
    feasible = checker.verify_travel_time(loc1, loc2)
    assert feasible, "Travel time verification failed"

    print("All tests passed!")


if __name__ == "__main__":
    test_location_checker()
