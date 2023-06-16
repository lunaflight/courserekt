import unittest
from src.data_cleaner.api import get_data


class MainTestCase(unittest.TestCase):
    def test_good_single_class(self):
        result = get_data("2223", "2", "ug", "CS2030S")
        self.assertTrue(result['code'] == 'CS2030S')
        self.assertTrue(result['classes'] ==
                        {'L1': [{'demand': 693, 'vacancy': 700},
                                {'demand': 52, 'vacancy': 31},
                                {'demand': 18, 'vacancy': 7},
                                {'demand': 6, 'vacancy': 2}]})
        self.assertTrue(result['error'] is None)

    def test_good_multiple_class(self):
        result = get_data("2223", "2", "ug", "CS2102")
        self.assertTrue(result['code'] == 'CS2102')
        self.assertTrue(result['classes'] ==
                        {'L1': [{'demand': 419, 'vacancy': 230},
                                {'demand': 23, 'vacancy': 12},
                                {'demand': 21, 'vacancy': 10},
                                {'demand': 14, 'vacancy': 16}],
                         'L2': [{'demand': -1, 'vacancy': -1},
                                {'demand': 50, 'vacancy': 23},
                                {'demand': 11, 'vacancy': 5},
                                {'demand': 15, 'vacancy': 15}]})
        self.assertTrue(result['error'] is None)

    def test_good_first_page_class(self):
        result = get_data("2223", "2", "ug", "PF1101")
        self.assertTrue(result['code'] == 'PF1101')
        self.assertTrue(result['classes'] ==
                        {'L1': [{'demand': 8, 'vacancy': 147},
                                {'demand': 8, 'vacancy': 140},
                                {'demand': 33, 'vacancy': 147},
                                {'demand': 33, 'vacancy': 116}]})
        self.assertTrue(result['error'] is None)

    def test_good_cut_into_2_class(self):
        result = get_data("2223", "2", "ug", "YSC4229")
        self.assertTrue(result['code'] == 'YSC4229')
        self.assertTrue(result['classes'] ==
                        {'E1': [{'demand': 13, 'vacancy': 16},
                                {'demand': 1, 'vacancy': 5},
                                {'demand': -1, 'vacancy': -1},
                                {'demand': -1, 'vacancy': -1}]})
        self.assertTrue(result['error'] is None)

    def test_good_graduate_class(self):
        result = get_data("2223", "2", "gd", "CS6208")
        self.assertTrue(result['code'] == 'CS6208')
        self.assertTrue(result['classes'] ==
                        {'L1': [{'demand': 26, 'vacancy': 18},
                                {'demand': 16, 'vacancy': 8},
                                {'demand': 15, 'vacancy': 11},
                                {'demand': 10, 'vacancy': 1}]})
        self.assertTrue(result['error'] is None)

    def test_bad_year(self):
        result = get_data("1819", "2", "ug", "CS2030S")
        self.assertTrue(result['error'] is not None)

    def test_bad_semester(self):
        result = get_data("2223", "3", "ug", "CS2030S")
        self.assertTrue(result['error'] is not None)

    def test_bad_undergraduate_graduate_type(self):
        result = get_data("2223", "2", "xd", "CS2030S")
        self.assertTrue(result['error'] is not None)

    def test_bad_course_code(self):
        result = get_data("2223", "2", "ug", "CC0092")
        self.assertTrue(result['error'] is not None)


if __name__ == '__main__':
    unittest.main()
