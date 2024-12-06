#!/usr/bin/env python
"""Tests for `t_object` package."""
import os
import unittest
from datetime import date, datetime, timedelta

from t_object.utils.logger import logger
from tests.models.complex_test_model import Car, Driver
from tests.models.datetime_test_model import Patient


class TestTObject(unittest.TestCase):
    """Smoke tests of the package."""

    def setUp(self):
        """Set up test."""
        self.patient = Patient(name="John Doe", age=42, birth_date=datetime(1979, 1, 1))
        self.car = Car(
            model="Tesla Model S",
            car_release_date=date(2012, 6, 22),
            price=79999.99,
            driver=[
                Driver(
                    name="Elon Musk",
                    age=49,
                    driving_experience=timedelta(days=365 * 30),
                    last_driving_date=datetime(2021, 1, 1),
                ),
                Driver(
                    name="Jeff Bezos",
                    age=57,
                    driving_experience=timedelta(days=365 * 20),
                    last_driving_date=datetime(2021, 1, 1),
                ),
            ],
        )
        self.output_dir = os.path.join(os.getcwd(), "output")

    def test_export(self):
        """Test the export of the object."""
        self.patient.save_to_json_file(os.path.join(self.output_dir, "patient.json")),
        self.car.save_to_json_file(os.path.join(self.output_dir, "car.json"))

    def test_default_export(self):
        """Test the export of the object."""
        self.patient.save_to_json_file(),
        self.car.save_to_json_file()
        self.car.save_to_json_file()
        self.car.save_to_json_file()
        self.car.save_to_json_file()

    def test_export_some_fields(self):
        """Test the export of the object with some fields."""
        file = self.patient.save_to_json_file(include_fields=["name", "age"])
        print(Patient.load_from_json_file(file))

    def test_import(self):
        """Test the import of the object."""
        self.patient.save_to_json_file(os.path.join(self.output_dir, "patient.json")),
        self.car.save_to_json_file(os.path.join(self.output_dir, "car.json"))
        patient = Patient.load_from_json_file(os.path.join(self.output_dir, "patient.json"))
        car = Car.load_from_json_file(os.path.join(self.output_dir, "car.json"))
        self.assertEqual(self.patient, patient)
        self.assertEqual(self.car, car)

    def test_logging(self):
        """Test the logging of the object."""
        logger.info(self.patient.pretty_string())
        logger.info(self.car.pretty_string())
        self.assertTrue(True)

    def test_list(self):
        """Test the list of the object."""
        cars = [self.car, self.car, self.car]
        Car.save_objects_list_to_json_file(cars, "cars.json")
        cars_json = Car.load_objects_list_from_json_file("cars.json")
        print(cars_json)
        self.assertEqual(cars, cars_json)
