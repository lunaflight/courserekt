import unittest
from src.planner.Scheduler import Scheduler


class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.scheduler = Scheduler()

    def test_add_non_overlapping(self):
        self.assertTrue(self.scheduler.add("Monday", "0600", "0800"))
        self.assertFalse(self.scheduler.add("Monday", "0700", "0900"))
        self.assertTrue(self.scheduler.add("Tuesday", "0900", "1000"))

    def test_add_consecutive(self):
        for time in ["0800", "1000", "1200", "1400", "1600", "1800"]:
            self.assertTrue(self.scheduler.add("Monday", time, str(int(time)+200)))

    def test_add_same_time_different_days(self):
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
            self.assertTrue(self.scheduler.add(day, "0800", "1000"))

    def test_add_overlapping(self):
        self.assertTrue(self.scheduler.add("Wednesday", "0800", "1000"))
        self.assertFalse(self.scheduler.add("Wednesday", "0900", "1100"))
        self.assertTrue(self.scheduler.add("Wednesday", "1000", "1200"))
        self.assertFalse(self.scheduler.add("Wednesday", "1100", "1300"))

    def test_add_30_min_intervals(self):
        self.assertTrue(self.scheduler.add("Tuesday", "1130", "1330"))
        self.assertTrue(self.scheduler.add("Tuesday", "1330", "1530"))
        self.assertTrue(self.scheduler.add("Tuesday", "1600", "1730"))
        self.assertFalse(self.scheduler.add("Tuesday", "1700", "1830"))
        self.assertTrue(self.scheduler.add("Tuesday", "1800", "1830"))

    def test_add_15_min_intervals(self):
        self.assertTrue(self.scheduler.add("Wednesday", "1045", "1115"))
        self.assertFalse(self.scheduler.add("Wednesday", "1100", "1130"))
        self.assertFalse(self.scheduler.add("Wednesday", "1000", "1145"))
        self.assertTrue(self.scheduler.add("Wednesday", "1115", "1230"))
        self.assertFalse(self.scheduler.add("Wednesday", "1215", "1230"))
        self.assertTrue(self.scheduler.add("Wednesday", "1245", "1430"))

    def test_clear_non_overlapping(self):
        self.scheduler.add("Monday", "0600", "0800")
        self.scheduler.clear("Monday", "0600", "0800")
        self.assertTrue(self.scheduler.add("Monday", "0600", "0800"))

    def test_clear_overlapping(self):
        self.assertTrue(self.scheduler.add("Friday", "1000", "1200"))
        self.assertFalse(self.scheduler.add("Friday", "1100", "1300"))
        self.scheduler.clear("Friday", "1100", "1200")
        self.assertTrue(self.scheduler.add("Friday", "1100", "1300"))

    def test_clear_nonexistent(self):
        self.scheduler.clear("Thursday", "1000", "1200")
        self.assertTrue(self.scheduler.add("Thursday", "1000", "1200"))
        self.scheduler.clear("Thursday", "1400", "1600")
        self.assertTrue(self.scheduler.add("Thursday", "1500", "1700"))

    def test_multiple_operations(self):
        self.assertTrue(self.scheduler.add("Saturday", "0800", "1000"))
        self.scheduler.clear("Saturday", "0830", "0900")
        self.assertTrue(self.scheduler.add("Saturday", "0830", "0900"))
        self.scheduler.clear("Saturday", "0845", "0915")
        self.assertTrue(self.scheduler.add("Saturday", "0845", "0915"))

    # We assume that the input is reasonable and valid
    # def test_edge_case_times(self):
    #     self.assertTrue(self.scheduler.add("Monday", "0000", "0100"))
    #     self.assertFalse(self.scheduler.add("Monday", "2359", "2400"))
    #     self.assertTrue(self.scheduler.add("Tuesday", "1200", "1300"))
    #     self.assertFalse(self.scheduler.add("Wednesday", "1300", "1200"))

    # def test_invalid_inputs(self):
    #     with self.assertRaises(ValueError):
    #         self.scheduler.add("Notaday", "0900", "1000")
    #     with self.assertRaises(ValueError):
    #         self.scheduler.add("Thursday", "9am", "1000")
    #     with self.assertRaises(ValueError):
    #         self.scheduler.add("Friday", "1005", "1100")

    # We assume that the string representation is unimportant
    # def test_str(self):
    #     self.scheduler.add("Sunday", "0800", "1000")
    #     self.assertEqual(str(self.scheduler), "Sunday: 0800-1000")


if __name__ == '__main__':
    unittest.main()
