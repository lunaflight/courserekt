import unittest
from src.planner.Scheduler import Scheduler


class TestScheduler(unittest.TestCase):
    def test_fail(self):
        self.assertTrue(False)

    def setUp(self):
        self.scheduler = Scheduler()

    def test_add(self):
        self.assertTrue(self.scheduler.add("Monday", "0600", "0800"))
        self.assertFalse(self.scheduler.add("Monday", "0700", "0900"))
        self.assertTrue(self.scheduler.add("Tuesday", "0900", "1000"))

    def test_clear(self):
        self.scheduler.add("Monday", "0600", "0800")
        self.scheduler.clear("Monday", "0600", "0800")
        self.assertTrue(self.scheduler.add("Monday", "0600", "0800"))

if __name__ == '__main__':
    unittest.main()
