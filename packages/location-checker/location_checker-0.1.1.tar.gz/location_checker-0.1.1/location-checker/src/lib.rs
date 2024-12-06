use chrono::{DateTime, Utc};
use country_boundaries::{CountryBoundaries, LatLon, BOUNDARIES_ODBL_360X180};
use geo::{Point, Haversine, Distance};
use once_cell::sync::OnceCell;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyModule;

static GLOBAL_BOUNDARIES: OnceCell<CountryBoundaries> = OnceCell::new();
const MAX_REALISTIC_SPEED_KMH: f64 = 900.0;

#[pyclass]
struct Location {
    latitude: f64,
    longitude: f64,
    timestamp: Option<DateTime<Utc>>, // Use Option for an optional field
}

#[pymethods]
impl Location {
    /// Constructor for `Location`.
    #[new]
    #[pyo3(signature = (latitude, longitude, timestamp=None))]
    fn new(latitude: f64, longitude: f64, timestamp: Option<&str>) -> PyResult<Self> {
        // Validate latitude and longitude ranges.
        if !(latitude >= -90.0 && latitude <= 90.0) {
            return Err(PyValueError::new_err("Latitude must be between -90 and 90."));
        }
        if !(longitude >= -180.0 && longitude <= 180.0) {
            return Err(PyValueError::new_err("Longitude must be between -180 and 180."));
        }

        // Parse and validate the timestamp if provided.
        let parsed_timestamp = if let Some(ts) = timestamp {
            Some(
                DateTime::parse_from_rfc3339(ts)
                    .map_err(|_| PyValueError::new_err("Invalid datetime format. Expected RFC 3339 format."))
                    .map(|dt| dt.with_timezone(&Utc))?,
            )
        } else {
            None
        };

        Ok(Location {
            latitude,
            longitude,
            timestamp: parsed_timestamp,
        })
    }
}

#[pyclass]
struct LocationChecker;

#[pymethods]
impl LocationChecker {
    #[new]
    fn new() -> PyResult<Self> {
        // Ensure boundaries are loaded during class initialization.
        Self::load_boundaries()?;
        Ok(LocationChecker {})
    }


    #[staticmethod]
    fn load_boundaries() -> PyResult<()> {
        if GLOBAL_BOUNDARIES.get().is_none() {
            let boundaries = CountryBoundaries::from_reader(BOUNDARIES_ODBL_360X180)
                .map_err(|_| PyValueError::new_err("Failed to load boundaries. Ensure the file is accessible."))?;
            GLOBAL_BOUNDARIES.set(boundaries).map_err(|_| {
                PyValueError::new_err("Unexpected error: boundaries were already initialized.")
            })?;
        }
        Ok(())
    }

    fn get_country(&self, location: &Location) -> PyResult<Vec<String>> {
        let boundaries = GLOBAL_BOUNDARIES.get().ok_or_else(|| {
            PyValueError::new_err("Boundaries not loaded. Please call `load_boundaries()`.")
        })?;

        let point = LatLon::new(location.latitude, location.longitude)
            .map_err(|_| PyValueError::new_err("Invalid LatLon values provided."))?;

        let country_ids: Vec<String> = boundaries
            .ids(point)
            .iter()
            .map(|&s| s.to_string())
            .collect();

        Ok(country_ids)
    }

    fn calculate_distance(&self, location1: &Location, location2: &Location) -> PyResult<f64> {
        let point1 = Point::new(location1.longitude, location1.latitude);
        let point2 = Point::new(location2.longitude, location2.latitude);
        Ok(Haversine::distance(point1, point2))
    }

    fn verify_travel_time(&self, start_location: &Location, end_location: &Location) -> PyResult<bool> {
        let start_time = start_location.timestamp.ok_or_else(|| {
            PyValueError::new_err("Start location must have a valid timestamp.")
        })?;
        let end_time = end_location.timestamp.ok_or_else(|| {
            PyValueError::new_err("End location must have a valid timestamp.")
        })?;

        let time_hours = (end_time - start_time).num_seconds() as f64 / 3600.0; // Convert seconds to hours
        let distance = self.calculate_distance(start_location, end_location)?;

        let max_distance_possible = MAX_REALISTIC_SPEED_KMH * time_hours;
        Ok(distance <= max_distance_possible * 1000.0) // Convert km to meters
    }
}



#[pymodule]
fn location_checker(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Location>()?;
    m.add_class::<LocationChecker>()?;
    Ok(())
}
