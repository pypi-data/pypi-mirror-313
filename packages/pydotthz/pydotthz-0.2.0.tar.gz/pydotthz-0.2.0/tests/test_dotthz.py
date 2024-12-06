import unittest
from dotthz import DotthzFile, DotthzMeasurement, DotthzMetaData
import numpy as np
from tempfile import NamedTemporaryFile
import os


class TestDotthzFile(unittest.TestCase):

    def test_copy_and_compare_dotthz_files(self):
        paths = [
            "../test_files/PVDF_520um.thz",
            "../test_files/2_VariableTemperature.thz",
        ]
        for path in paths:
            # Create a temporary file to save the copy
            with NamedTemporaryFile(delete=False) as temp_file:
                copy_file_path = temp_file.name

            # Load data from the original file
            with DotthzFile(path) as original_dotthz_file, DotthzFile(copy_file_path, "w") as copied_dotthz_file:
                original_measurements = original_dotthz_file.get_measurements()
                for name, measurement in original_measurements.items():
                    # Save the data to the new temporary file
                    copied_dotthz_file.write_measurement(name, measurement)

            # Load data from the new copy file
            with DotthzFile(path) as copied_dotthz_file:

                # Compare the original and copied Dotthz structures
                self.assertEqual(len(original_measurements), len(copied_dotthz_file.get_measurements()))

                for group_name, original_measurement in original_measurements.items():
                    copied_measurement = copied_dotthz_file.get_measurement(group_name)
                    self.assertIsNotNone(copied_measurement)

                    # Compare metadata fields
                    self.assertEqual(original_measurement.meta_data.user, copied_measurement.meta_data.user)
                    self.assertEqual(original_measurement.meta_data.email, copied_measurement.meta_data.email)
                    self.assertEqual(original_measurement.meta_data.orcid, copied_measurement.meta_data.orcid)
                    self.assertEqual(original_measurement.meta_data.institution,
                                     copied_measurement.meta_data.institution)
                    self.assertEqual(original_measurement.meta_data.description,
                                     copied_measurement.meta_data.description)
                    self.assertEqual(original_measurement.meta_data.version, copied_measurement.meta_data.version)
                    self.assertEqual(original_measurement.meta_data.mode, copied_measurement.meta_data.mode)
                    self.assertEqual(original_measurement.meta_data.instrument, copied_measurement.meta_data.instrument)
                    self.assertEqual(original_measurement.meta_data.time, copied_measurement.meta_data.time)
                    self.assertEqual(original_measurement.meta_data.date, copied_measurement.meta_data.date)

                    # Compare metadata key-value pairs
                    self.assertEqual(original_measurement.meta_data.md, copied_measurement.meta_data.md)

                    # Compare datasets
                    self.assertEqual(len(original_measurement.datasets), len(copied_measurement.datasets))
                    for dataset_name, original_dataset in original_measurement.datasets.items():
                        copied_dataset = copied_measurement.datasets.get(dataset_name)
                        self.assertIsNotNone(copied_dataset)
                        np.testing.assert_array_equal(original_dataset, copied_dataset)

                # Clean up temporary file
                os.remove(copy_file_path)

    def test_dotthz_save_and_load(self):
        with NamedTemporaryFile(delete=False) as temp_file:
            path = temp_file.name

        # Initialize test data for Dotthz
        datasets = {
            "ds1": np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float32)
        }
        meta_data = DotthzMetaData(
            user="Test User",
            email="test@example.com",
            orcid="0000-0001-2345-6789",
            institution="Test Institute",
            description="Test description",
            md={"md1": "Thickness (mm)"},
            version="1.00",
            mode="Test mode",
            instrument="Test instrument",
            time="12:34:56",
            date="2024-11-08"
        )

        measurements = {
            "Measurement 1": DotthzMeasurement(datasets=datasets, meta_data=meta_data)
        }

        with DotthzFile(path, "w") as file_to_write:
            for name, measurement in measurements.items():
                file_to_write.write_measurement(name, measurement)

        # Load from the temporary file
        with DotthzFile(path) as loaded_file:
            # Compare original and loaded data
            self.assertEqual(len(measurements), len(loaded_file.get_measurements()))

            for group_name, measurement in file_to_write.get_measurements().items():
                loaded_measurement = loaded_file.get_measurement(group_name)
                self.assertIsNotNone(loaded_measurement)

                # Compare metadata fields
                self.assertEqual(measurement.meta_data.user, loaded_measurement.meta_data.user)
                self.assertEqual(measurement.meta_data.email, loaded_measurement.meta_data.email)
                self.assertEqual(measurement.meta_data.orcid, loaded_measurement.meta_data.orcid)
                self.assertEqual(measurement.meta_data.institution, loaded_measurement.meta_data.institution)
                self.assertEqual(measurement.meta_data.description, loaded_measurement.meta_data.description)
                self.assertEqual(measurement.meta_data.version, loaded_measurement.meta_data.version)
                self.assertEqual(measurement.meta_data.mode, loaded_measurement.meta_data.mode)
                self.assertEqual(measurement.meta_data.instrument, loaded_measurement.meta_data.instrument)
                self.assertEqual(measurement.meta_data.time, loaded_measurement.meta_data.time)
                self.assertEqual(measurement.meta_data.date, loaded_measurement.meta_data.date)

                # Compare metadata's key-value pairs
                self.assertEqual(measurement.meta_data.md, loaded_measurement.meta_data.md)

                # Compare datasets
                self.assertEqual(len(measurement.datasets), len(loaded_measurement.datasets))
                for dataset_name, dataset in measurement.datasets.items():
                    loaded_dataset = loaded_measurement.datasets.get(dataset_name)
                    self.assertIsNotNone(loaded_dataset)
                    np.testing.assert_array_equal(dataset, loaded_dataset)

            # Clean up temporary file
            os.remove(path)


if __name__ == "__main__":
    unittest.main()
