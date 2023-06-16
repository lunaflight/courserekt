import unittest
from src.data_cleaner.api import get_data


class MainTestCase(unittest.TestCase):
    def assert_known_2223_2_ug_cs2030s_result(self, result):
        self.assertTrue(result['code'] == 'CS2030S')
        self.assertTrue(result['classes'] ==
{'L1': [{'demand': 693, 'vacancy': 700, 'successful_main': 693, 'successful_reserve': 0, 'quota_exceeded': 0, 'timetable_clashes': 0, 'workload_exceeded': 0, 'others': 0}, {'demand': 52, 'vacancy': 31, 'successful_main': 31, 'successful_reserve': 0, 'quota_exceeded': 21, 'timetable_clashes': 0, 'workload_exceeded': 0, 'others': 0}, {'demand': 18, 'vacancy': 7, 'successful_main': 7, 'successful_reserve': 0, 'quota_exceeded': 11, 'timetable_clashes': 0, 'workload_exceeded': 0, 'others': 0}, {'demand': 6, 'vacancy': 2, 'successful_main': 0, 'successful_reserve': 0, 'quota_exceeded': 0, 'timetable_clashes': 0, 'workload_exceeded': 0, 'others': 6}]})
        self.assertTrue(result['error'] is None)

    def test_good_single_class(self):
        result = get_data("2223", "2", "ug", "CS2030S")
        self.assert_known_2223_2_ug_cs2030s_result(result)

    def test_course_capitalisation(self):
        result = get_data("2223", "2", "ug", "cs2030s")
        self.assert_known_2223_2_ug_cs2030s_result(result)

    def test_mixed_course_capitalisation(self):
        result = get_data("2223", "2", "ug", "cS2030S")
        self.assert_known_2223_2_ug_cs2030s_result(result)

    def test_type_capitalisation(self):
        result = get_data("2223", "2", "UG", "CS2030S")
        self.assert_known_2223_2_ug_cs2030s_result(result)

    def test_mixed_type_capitalisation(self):
        result = get_data("2223", "2", "uG", "CS2030S")
        self.assert_known_2223_2_ug_cs2030s_result(result)

    def test_slash_in_year(self):
        result = get_data("22/23", "2", "ug", "CS2030S")
        self.assert_known_2223_2_ug_cs2030s_result(result)

    def test_space_in_year(self):
        result = get_data("22 23", "2", "ug", "CS2030S")
        self.assert_known_2223_2_ug_cs2030s_result(result)

    def test_spaces_in_strings(self):
        result = get_data("  2223 ", " 2", " ug", "CS2030S ")
        self.assert_known_2223_2_ug_cs2030s_result(result)

    def test_num_representation_of_year(self):
        result = get_data(2223, " 2", " ug", "CS2030S ")
        self.assert_known_2223_2_ug_cs2030s_result(result)

    def test_num_representation_of_semester(self):
        result = get_data("2223", 2, " ug", "CS2030S ")
        self.assert_known_2223_2_ug_cs2030s_result(result)

    def test_good_multiple_class(self):
        result = get_data("2223", "2", "ug", "CS2102")
        self.assertTrue(result['code'] == 'CS2102')
        self.assertTrue(result['classes'] ==
{'L1': [{'demand': 419, 'vacancy': 230, 'successful_main': 230, 'successful_reserve': 0, 'quota_exceeded': 188, 'timetable_clashes': 1, 'workload_exceeded': 0, 'others': 0}, {'demand': 23, 'vacancy': 12, 'successful_main': 12, 'successful_reserve': 0, 'quota_exceeded': 11, 'timetable_clashes': 0, 'workload_exceeded': 0, 'others': 0}, {'demand': 21, 'vacancy': 10, 'successful_main': 10, 'successful_reserve': 0, 'quota_exceeded': 11, 'timetable_clashes': 0, 'workload_exceeded': 0, 'others': 0}, {'demand': 14, 'vacancy': 16, 'successful_main': 13, 'successful_reserve': 0, 'quota_exceeded': 0, 'timetable_clashes': 0, 'workload_exceeded': 0, 'others': 1}], 'L2': [{'demand': -1, 'vacancy': -1, 'successful_main': -1, 'successful_reserve': -1, 'quota_exceeded': -1, 'timetable_clashes': -1, 'workload_exceeded': -1, 'others': -1}, {'demand': 50, 'vacancy': 23, 'successful_main': 23, 'successful_reserve': 0, 'quota_exceeded': 27, 'timetable_clashes': 0, 'workload_exceeded': 0, 'others': 0}, {'demand': 11, 'vacancy': 5, 'successful_main': 5, 'successful_reserve': 0, 'quota_exceeded': 6, 'timetable_clashes': 0, 'workload_exceeded': 0, 'others': 0}, {'demand': 15, 'vacancy': 15, 'successful_main': 15, 'successful_reserve': 0, 'quota_exceeded': 0, 'timetable_clashes': 0, 'workload_exceeded': 0, 'others': 0}]})
        self.assertTrue(result['error'] is None)

    def test_good_first_page_class(self):
        result = get_data("2223", "2", "ug", "PF1101")
        self.assertTrue(result['code'] == 'PF1101')
        self.assertTrue(result['classes'] ==
                        {'L1': [{'demand': 8, 'vacancy': 147, 'successful_main': 8, 'successful_reserve': 0, 'quota_exceeded': 0, 'timetable_clashes': 0, 'workload_exceeded': 0, 'others': 0}, {'demand': 8, 'vacancy': 140, 'successful_main': 8, 'successful_reserve': 0, 'quota_exceeded': 0, 'timetable_clashes': 0, 'workload_exceeded': 0, 'others': 0}, {'demand': 33, 'vacancy': 147, 'successful_main': 33, 'successful_reserve': 0, 'quota_exceeded': 0, 'timetable_clashes': 0, 'workload_exceeded': 0, 'others': 0}, {'demand': 33, 'vacancy': 116, 'successful_main': 32, 'successful_reserve': 4, 'quota_exceeded': 0, 'timetable_clashes': 0, 'workload_exceeded': 0, 'others': 1}]})
        self.assertTrue(result['error'] is None)

    def test_good_cut_into_2_class(self):
        result = get_data("2223", "2", "ug", "YSC4229")
        self.assertTrue(result['code'] == 'YSC4229')
        self.assertTrue(result['classes'] ==
{'E1': [{'demand': 13, 'vacancy': 16, 'successful_main': 13, 'successful_reserve': 2, 'quota_exceeded': 0, 'timetable_clashes': 0, 'workload_exceeded': 0, 'others': 0}, {'demand': 1, 'vacancy': 5, 'successful_main': 1, 'successful_reserve': 0, 'quota_exceeded': 0, 'timetable_clashes': 0, 'workload_exceeded': 0, 'others': 0}, {'demand': -1, 'vacancy': -1, 'successful_main': -1, 'successful_reserve': -1, 'quota_exceeded': -1, 'timetable_clashes': -1, 'workload_exceeded': -1, 'others': -1}, {'demand': -1, 'vacancy': -1, 'successful_main': -1, 'successful_reserve': -1, 'quota_exceeded': -1, 'timetable_clashes': -1, 'workload_exceeded': -1, 'others': -1}]})
        self.assertTrue(result['error'] is None)

    def test_good_graduate_class(self):
        result = get_data("2223", "2", "gd", "CS6208")
        self.assertTrue(result['code'] == 'CS6208')
        self.assertTrue(result['classes'] ==
                        {'L1': [{'demand': 26, 'vacancy': 18, 'successful_main': 18, 'successful_reserve': 0, 'quota_exceeded': 8, 'timetable_clashes': 0, 'workload_exceeded': 0, 'others': 0}, {'demand': 16, 'vacancy': 8, 'successful_main': 8, 'successful_reserve': 0, 'quota_exceeded': 8, 'timetable_clashes': 0, 'workload_exceeded': 0, 'others': 0}, {'demand': 15, 'vacancy': 11, 'successful_main': 11, 'successful_reserve': 0, 'quota_exceeded': 4, 'timetable_clashes': 0, 'workload_exceeded': 0, 'others': 0}, {'demand': 10, 'vacancy': 1, 'successful_main': 1, 'successful_reserve': 0, 'quota_exceeded': 9, 'timetable_clashes': 0, 'workload_exceeded': 0, 'others': 0}]})
        self.assertTrue(result['error'] is None)

    def test_bad_year(self):
        result = get_data("1819", "2", "ug", "CS2030S")
        self.assertTrue(result['error'] is not None)

    def test_bad_semester_0(self):
        result = get_data("2223", "0", "ug", "CS2030S")
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

    def test_missing_year(self):
        result = get_data("", "2", "ug", "CS2030S")
        self.assertTrue(result['error'] is not None)

    def test_missing_semester(self):
        result = get_data("2223", "", "ug", "CS2030S")
        self.assertTrue(result['error'] is not None)

    def test_missing_type(self):
        result = get_data("2223", "2", "", "CS2030S")
        self.assertTrue(result['error'] is not None)

    def test_missing_course(self):
        result = get_data("2223", "2", "ug", "")
        self.assertTrue(result['error'] is not None)


if __name__ == '__main__':
    unittest.main()
