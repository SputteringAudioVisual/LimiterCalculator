import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
AMP_DATABASE = ROOT / "dataBase" / "amplifierDataBase"
DRIVER_DATABASE = ROOT / "dataBase" / "driverDataBase"
META_KEYS = {"Brand", "Model", "Sensitivity"}
SENSITIVITY_UNITS = {"V sens", "dBu sens", "X Factor", "DB"}


class DatabaseTests(unittest.TestCase):
    def test_amplifier_files_follow_schema(self):
        files = sorted(AMP_DATABASE.glob("*.json"))
        self.assertTrue(files, "No amplifier JSON files found")

        for path in files:
            with self.subTest(path=path.name):
                data = json.loads(path.read_text(encoding="utf-8"))
                self.assertTrue(data["Brand"])
                self.assertTrue(data["Model"])
                self.assertIsInstance(data["Sensitivity"], (list, dict))

                modes = [key for key in data if key not in META_KEYS]
                self.assertTrue(modes, "Amplifier has no operating modes")
                for mode in modes:
                    impedances = data[mode]["Impedance"]
                    powers = data[mode]["Power"]
                    self.assertEqual(len(impedances), len(powers))
                    self.assertTrue(all(value > 0 for value in impedances))
                    self.assertTrue(all(value > 0 for value in powers))

                if isinstance(data["Sensitivity"], list):
                    self.assertTrue(data["Sensitivity"])
                    for option in data["Sensitivity"]:
                        self.assertTrue(option["label"])
                        self.assertIn(option["unit"], SENSITIVITY_UNITS)
                        self.assertIsInstance(option["value"], (int, float))

    def test_driver_files_follow_schema(self):
        files = sorted(DRIVER_DATABASE.glob("*.json"))
        self.assertTrue(files, "No driver JSON files found")

        for path in files:
            with self.subTest(path=path.name):
                data = json.loads(path.read_text(encoding="utf-8"))
                self.assertTrue(data["Brand"])
                self.assertTrue(data["Model"])
                self.assertGreater(data["Impedance"], 0)
                self.assertGreater(data["Power"], 0)


if __name__ == "__main__":
    unittest.main()
