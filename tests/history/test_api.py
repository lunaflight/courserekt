import unittest
from src.history.api import get_data, CourseData


class MainTestCase(unittest.TestCase):
    def assert_known_2223_2_ug_cs2030s_result(self, result: CourseData) -> None:
        try:
            expected_data = {
                "faculty": "School of Computing",
                "department": "Computer Science",
                "code": "CS2030S",
                "title": "Programming Methodology II",
                "classes": {
                    "L1": [
                        {
                            "ug": 580,
                            "gd": -1,
                            "dk": -1,
                            "ng": -1,
                            "cpe": -1,
                            "demand": 693,
                            "vacancy": 700,
                            "successful_main": 693,
                            "successful_reserve": 0,
                            "quota_exceeded": 0,
                            "timetable_clashes": 0,
                            "workload_exceeded": 0,
                            "others": 0
                        },
                        {
                            "ug": 24,
                            "gd": -1,
                            "dk": -1,
                            "ng": -1,
                            "cpe": -1,
                            "demand": 52,
                            "vacancy": 31,
                            "successful_main": 31,
                            "successful_reserve": 0,
                            "quota_exceeded": 21,
                            "timetable_clashes": 0,
                            "workload_exceeded": 0,
                            "others": 0
                        },
                        {
                            "ug": 3,
                            "gd": -1,
                            "dk": -1,
                            "ng": -1,
                            "cpe": -1,
                            "demand": 18,
                            "vacancy": 7,
                            "successful_main": 7,
                            "successful_reserve": 0,
                            "quota_exceeded": 11,
                            "timetable_clashes": 0,
                            "workload_exceeded": 0,
                            "others": 0
                        },
                        {
                            "ug": 0,
                            "gd": -1,
                            "dk": -1,
                            "ng": -1,
                            "cpe": -1,
                            "demand": 6,
                            "vacancy": 2,
                            "successful_main": 0,
                            "successful_reserve": 0,
                            "quota_exceeded": 0,
                            "timetable_clashes": 0,
                            "workload_exceeded": 0,
                            "others": 6
                        }
                    ]
                }
            }

            self.assertTrue(result == expected_data)
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_good_single_class(self) -> None:
        result = get_data("2223", "2", "ug", "CS2030S")
        self.assert_known_2223_2_ug_cs2030s_result(result)

    def test_course_capitalisation(self) -> None:
        result = get_data("2223", "2", "ug", "cs2030s")
        self.assert_known_2223_2_ug_cs2030s_result(result)

    def test_mixed_course_capitalisation(self) -> None:
        result = get_data("2223", "2", "ug", "cS2030S")
        self.assert_known_2223_2_ug_cs2030s_result(result)

    def test_type_capitalisation(self) -> None:
        result = get_data("2223", "2", "UG", "CS2030S")
        self.assert_known_2223_2_ug_cs2030s_result(result)

    def test_mixed_type_capitalisation(self) -> None:
        result = get_data("2223", "2", "uG", "CS2030S")
        self.assert_known_2223_2_ug_cs2030s_result(result)

    def test_slash_in_year(self) -> None:
        result = get_data("22/23", "2", "ug", "CS2030S")
        self.assert_known_2223_2_ug_cs2030s_result(result)

    def test_space_in_year(self) -> None:
        result = get_data("22 23", "2", "ug", "CS2030S")
        self.assert_known_2223_2_ug_cs2030s_result(result)

    def test_8_digit_year(self) -> None:
        result = get_data("20222023", "2", "ug", "CS2030S")
        self.assert_known_2223_2_ug_cs2030s_result(result)

    def test_8_digit_year_with_space(self) -> None:
        result = get_data("2022 2023", "2", "ug", "CS2030S")
        self.assert_known_2223_2_ug_cs2030s_result(result)

    def test_8_digit_year_with_slash(self) -> None:
        result = get_data("2022-2023", "2", "ug", "CS2030S")
        self.assert_known_2223_2_ug_cs2030s_result(result)

    def test_8_digit_year_with_dash(self) -> None:
        result = get_data("2022-2023", "2", "ug", "CS2030S")
        self.assert_known_2223_2_ug_cs2030s_result(result)

    def test_spaces_in_strings(self) -> None:
        result = get_data("  2223 ", " 2", " ug", "CS2030S ")
        self.assert_known_2223_2_ug_cs2030s_result(result)

    def test_num_representation_of_year(self) -> None:
        result = get_data(2223, "2", "ug", "CS2030S")
        self.assert_known_2223_2_ug_cs2030s_result(result)

    def test_num_representation_of_semester(self) -> None:
        result = get_data("2223", 2, "ug", "CS2030S")
        self.assert_known_2223_2_ug_cs2030s_result(result)

    def test_good_multiple_class(self) -> None:
        try:
            result = get_data("2223", "2", "ug", "CS2102")
            expected_data = {
                "faculty": "School of Computing",
                "department": "Computer Science",
                "code": "CS2102",
                "title": "Database Systems",
                "classes": {
                    "L1": [
                        {
                            "ug": 230,
                            "gd": -1,
                            "dk": -1,
                            "ng": -1,
                            "cpe": -1,
                            "demand": 419,
                            "vacancy": 230,
                            "successful_main": 230,
                            "successful_reserve": 0,
                            "quota_exceeded": 188,
                            "timetable_clashes": 1,
                            "workload_exceeded": 0,
                            "others": 0
                            },
                        {
                            "ug": 2,
                            "gd": -1,
                            "dk": -1,
                            "ng": -1,
                            "cpe": -1,
                            "demand": 23,
                            "vacancy": 12,
                            "successful_main": 12,
                            "successful_reserve": 0,
                            "quota_exceeded": 11,
                            "timetable_clashes": 0,
                            "workload_exceeded": 0,
                            "others": 0
                            },
                        {
                            "ug": 0,
                            "gd": -1,
                            "dk": -1,
                            "ng": -1,
                            "cpe": -1,
                            "demand": 21,
                            "vacancy": 10,
                            "successful_main": 10,
                            "successful_reserve": 0,
                            "quota_exceeded": 11,
                            "timetable_clashes": 0,
                            "workload_exceeded": 0,
                            "others": 0
                            },
                        {
                            "ug": 0,
                            "gd": -1,
                            "dk": -1,
                            "ng": -1,
                            "cpe": -1,
                            "demand": 14,
                            "vacancy": 16,
                            "successful_main": 13,
                            "successful_reserve": 0,
                            "quota_exceeded": 0,
                            "timetable_clashes": 0,
                            "workload_exceeded": 0,
                            "others": 1
                        }
                    ],

                    "L2": [
                        {
                            "ug": -1,
                            "gd": -1,
                            "dk": -1,
                            "ng": -1,
                            "cpe": -1,
                            "demand": -1,
                            "vacancy": -1,
                            "successful_main": -1,
                            "successful_reserve": -1,
                            "quota_exceeded": -1,
                            "timetable_clashes": -1,
                            "workload_exceeded": -1,
                            "others": -1
                            },
                        {
                            "ug": 18,
                            "gd": -1,
                            "dk": -1,
                            "ng": -1,
                            "cpe": -1,
                            "demand": 50,
                            "vacancy": 23,
                            "successful_main": 23,
                            "successful_reserve": 0,
                            "quota_exceeded": 27,
                            "timetable_clashes": 0,
                            "workload_exceeded": 0,
                            "others": 0
                            },
                        {
                            "ug": 0,
                            "gd": -1,
                            "dk": -1,
                            "ng": -1,
                            "cpe": -1,
                            "demand": 11,
                            "vacancy": 5,
                            "successful_main": 5,
                            "successful_reserve": 0,
                            "quota_exceeded": 6,
                            "timetable_clashes": 0,
                            "workload_exceeded": 0,
                            "others": 0
                            },
                        {
                            "ug": 0,
                            "gd": -1,
                            "dk": -1,
                            "ng": -1,
                            "cpe": -1,
                            "demand": 15,
                            "vacancy": 15,
                            "successful_main": 15,
                            "successful_reserve": 0,
                            "quota_exceeded": 0,
                            "timetable_clashes": 0,
                            "workload_exceeded": 0,
                            "others": 0
                        }
                    ]
                }
            }

            self.assertTrue(result == expected_data)
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_good_first_page_class(self) -> None:
        try:
            result = get_data("2223", "2", "ug", "PF1101")
            expected_data = {
                "faculty": "College of Design and Eng",
                "department": "Built Environment",
                "code": "PF1101",
                "title": "Fundamentals of Project Management",
                "classes": {
                    "L1": [
                        {
                            "ug": 132,
                            "gd": -1,
                            "dk": -1,
                            "ng": -1,
                            "cpe": -1,
                            "demand": 8,
                            "vacancy": 147,
                            "successful_main": 8,
                            "successful_reserve": 0,
                            "quota_exceeded": 0,
                            "timetable_clashes": 0,
                            "workload_exceeded": 0,
                            "others": 0
                            },
                        {
                            "ug": 132,
                            "gd": -1,
                            "dk": -1,
                            "ng": -1,
                            "cpe": -1,
                            "demand": 8,
                            "vacancy": 140,
                            "successful_main": 8,
                            "successful_reserve": 0,
                            "quota_exceeded": 0,
                            "timetable_clashes": 0,
                            "workload_exceeded": 0,
                            "others": 0
                            },
                        {
                            "ug": 132,
                            "gd": -1,
                            "dk": -1,
                            "ng": -1,
                            "cpe": -1,
                            "demand": 33,
                            "vacancy": 147,
                            "successful_main": 33,
                            "successful_reserve": 0,
                            "quota_exceeded": 0,
                            "timetable_clashes": 0,
                            "workload_exceeded": 0,
                            "others": 0
                            },
                        {
                            "ug": 114,
                            "gd": -1,
                            "dk": -1,
                            "ng": -1,
                            "cpe": -1,
                            "demand": 33,
                            "vacancy": 116,
                            "successful_main": 32,
                            "successful_reserve": 4,
                            "quota_exceeded": 0,
                            "timetable_clashes": 0,
                            "workload_exceeded": 0,
                            "others": 1
                            }
                    ]
                }
            }

            self.assertTrue(result == expected_data)
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_good_cut_into_2_class(self) -> None:
        try:
            result = get_data("2223", "2", "ug", "YSC4229")
            expected_data = {
                "faculty": "Yale-NUS College",
                "department": "Yale-NUS College",
                "code": "YSC4229",
                "title": "Molecular Neuroscience - Genes, Brains, and Behaviour",
                "classes": {
                    "E1": [
                        {
                            "ug": 16,
                            "gd": -1,
                            "dk": -1,
                            "ng": 1,
                            "cpe": -1,
                            "demand": 13,
                            "vacancy": 16,
                            "successful_main": 13,
                            "successful_reserve": 2,
                            "quota_exceeded": 0,
                            "timetable_clashes": 0,
                            "workload_exceeded": 0,
                            "others": 0
                            },
                        {
                            "ug": 4,
                            "gd": -1,
                            "dk": -1,
                            "ng": 1,
                            "cpe": -1,
                            "demand": 1,
                            "vacancy": 5,
                            "successful_main": 1,
                            "successful_reserve": 0,
                            "quota_exceeded": 0,
                            "timetable_clashes": 0,
                            "workload_exceeded": 0,
                            "others": 0
                            },
                        {
                            "ug": 4,
                            "gd": -1,
                            "dk": -1,
                            "ng": 1,
                            "cpe": -1,
                            "demand": 0,
                            "vacancy": 4,
                            "successful_main": 0,
                            "successful_reserve": 0,
                            "quota_exceeded": 0,
                            "timetable_clashes": 0,
                            "workload_exceeded": 0,
                            "others": 0
                            },
                        {
                            "ug": 4,
                            "gd": -1,
                            "dk": -1,
                            "ng": 1,
                            "cpe": -1,
                            "demand": 0,
                            "vacancy": 4,
                            "successful_main": 0,
                            "successful_reserve": 0,
                            "quota_exceeded": 0,
                            "timetable_clashes": 0,
                            "workload_exceeded": 0,
                            "others": 0
                            }
                    ]
                }
            }

            self.assertTrue(result == expected_data)
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_good_graduate_class(self) -> None:
        try:
            result = get_data("2223", "2", "gd", "CS6208")
            expected_data = {
                "faculty": "School of Computing",
                "department": "Computer Science",
                "code": "CS6208",
                "title": "Advanced Topics in Artificial Intelligence",
                "classes": {
                    "L1": [
                        {
                            "ug": -1,
                            "gd": 18,
                            "dk": -1,
                            "ng": -1,
                            "cpe": -1,
                            "demand": 26,
                            "vacancy": 18,
                            "successful_main": 18,
                            "successful_reserve": 0,
                            "quota_exceeded": 8,
                            "timetable_clashes": 0,
                            "workload_exceeded": 0,
                            "others": 0
                            },
                        {
                            "ug": -1,
                            "gd": 7,
                            "dk": -1,
                            "ng": -1,
                            "cpe": -1,
                            "demand": 16,
                            "vacancy": 8,
                            "successful_main": 8,
                            "successful_reserve": 0,
                            "quota_exceeded": 8,
                            "timetable_clashes": 0,
                            "workload_exceeded": 0,
                            "others": 0
                            },
                        {
                            "ug": -1,
                            "gd": 3,
                            "dk": -1,
                            "ng": -1,
                            "cpe": -1,
                            "demand": 15,
                            "vacancy": 11,
                            "successful_main": 11,
                            "successful_reserve": 0,
                            "quota_exceeded": 4,
                            "timetable_clashes": 0,
                            "workload_exceeded": 0,
                            "others": 0
                            },
                        {
                            "ug": -1,
                            "gd": 0,
                            "dk": -1,
                            "ng": -1,
                            "cpe": -1,
                            "demand": 10,
                            "vacancy": 1,
                            "successful_main": 1,
                            "successful_reserve": 0,
                            "quota_exceeded": 9,
                            "timetable_clashes": 0,
                            "workload_exceeded": 0,
                            "others": 0
                            }
                    ]
                }
            }

            self.assertTrue(result == expected_data)
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_good_omitted_vacancy(self) -> None:
        try:
            result = get_data("2223", "1", "ug", "LL4004V")
            expected_data = {
                "faculty": "Faculty of Law",
                "department": "FoL Dean's Office",
                "code": "LL4004V",
                "title": "Aviation Law & Policy",
                "classes": {
                    "E1": [
                        {
                            "ug": -1,
                            "gd": -1,
                            "dk": -1,
                            "ng": -1,
                            "cpe": -1,
                            "demand": -1,
                            "vacancy": -1,
                            "successful_main": -1,
                            "successful_reserve": -1,
                            "quota_exceeded": -1,
                            "timetable_clashes": -1,
                            "workload_exceeded": -1,
                            "others": -1
                            },
                        {
                            "ug": -1,
                            "gd": -1,
                            "dk": -1,
                            "ng": -1,
                            "cpe": -1,
                            "demand": 9,
                            "vacancy": 2147483647,
                            "successful_main": 9,
                            "successful_reserve": 5,
                            "quota_exceeded": 0,
                            "timetable_clashes": 0,
                            "workload_exceeded": 0,
                            "others": 0
                            },
                        {
                            "ug": -1,
                            "gd": -1,
                            "dk": -1,
                            "ng": -1,
                            "cpe": -1,
                            "demand": 8,
                            "vacancy": 2147483647,
                            "successful_main": 8,
                            "successful_reserve": 2,
                            "quota_exceeded": 0,
                            "timetable_clashes": 0,
                            "workload_exceeded": 0,
                            "others": 0
                            },
                        {
                            "ug": -1,
                            "gd": -1,
                            "dk": -1,
                            "ng": -1,
                            "cpe": -1,
                            "demand": 5,
                            "vacancy": 2147483647,
                            "successful_main": 5,
                            "successful_reserve": 1,
                            "quota_exceeded": 0,
                            "timetable_clashes": 0,
                            "workload_exceeded": 0,
                            "others": 0
                        }
                    ]
                }
            }

            self.assertTrue(result == expected_data)
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_good_hyphenated_vacancy(self) -> None:
        try:
            result = get_data("2223", "2", "ug", "CM3253")
            expected_data = {
                "faculty": "Faculty of Science",
                "department": "Chemistry",
                "code": "CM3253",
                "title": "Materials Chemistry 1",
                "classes": {
                    "L1": [
                        {
                            "ug": 2147483647,
                            "gd": -1,
                            "dk": -1,
                            "ng": 2147483647,
                            "cpe": -1,
                            "demand": 6,
                            "vacancy": 2147483647,
                            "successful_main": 6,
                            "successful_reserve": 0,
                            "quota_exceeded": 0,
                            "timetable_clashes": 0,
                            "workload_exceeded": 0,
                            "others": 0
                            },
                        {
                            "ug": 2147483647,
                            "gd": -1,
                            "dk": -1,
                            "ng": 2147483647,
                            "cpe": -1,
                            "demand": 3,
                            "vacancy": 2147483647,
                            "successful_main": 3,
                            "successful_reserve": 0,
                            "quota_exceeded": 0,
                            "timetable_clashes": 0,
                            "workload_exceeded": 0,
                            "others": 0
                            },
                        {
                            "ug": 2147483647,
                            "gd": -1,
                            "dk": -1,
                            "ng": 2147483647,
                            "cpe": -1,
                            "demand": 2,
                            "vacancy": 2147483647,
                            "successful_main": 2,
                            "successful_reserve": 0,
                            "quota_exceeded": 0,
                            "timetable_clashes": 0,
                            "workload_exceeded": 0,
                            "others": 0
                            },
                        {
                            "ug": 2147483647,
                            "gd": -1,
                            "dk": -1,
                            "ng": 2147483647,
                            "cpe": -1,
                            "demand": 3,
                            "vacancy": 2147483647,
                            "successful_main": 3,
                            "successful_reserve": 0,
                            "quota_exceeded": 0,
                            "timetable_clashes": 0,
                            "workload_exceeded": 0,
                            "others": 0
                            }
                    ]
                }
            }

            self.assertTrue(result == expected_data)
        except Exception as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_bad_year(self) -> None:
        with self.assertRaises(ValueError):
            get_data("1819", "2", "ug", "CS2030S")

    def test_bad_semester_0(self) -> None:
        with self.assertRaises(ValueError):
            get_data("2223", "0", "ug", "CS2030S")

    def test_bad_semester(self) -> None:
        with self.assertRaises(ValueError):
            get_data("2223", "3", "ug", "CS2030S")

    def test_bad_undergraduate_graduate_type(self) -> None:
        with self.assertRaises(ValueError):
            get_data("2223", "2", "xd", "CS2030S")

    def test_bad_course_code(self) -> None:
        with self.assertRaises(ValueError):
            get_data("2223", "2", "ug", "CC0092")

    def test_missing_year(self) -> None:
        with self.assertRaises(ValueError):
            get_data("", "2", "ug", "CS2030S")

    def test_missing_semester(self) -> None:
        with self.assertRaises(ValueError):
            get_data("2223", "", "ug", "CS2030S")

    def test_missing_type(self) -> None:
        with self.assertRaises(ValueError):
            get_data("2223", "2", "", "CS2030S")

    def test_missing_course(self) -> None:
        with self.assertRaises(ValueError):
            get_data("2223", "2", "ug", "")


if __name__ == '__main__':
    unittest.main()
