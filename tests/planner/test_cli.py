import unittest
from src.planner.cli import parse_and_generate_url


class Test_CLI(unittest.TestCase):
    def test_valid_standard(self):
        parse_and_generate_url('2022-2023',
                               1,
                               ['CS3241'],
                               [],
                               dry_run=True)

    def test_valid_whitelist(self):
        parse_and_generate_url('2022-2023',
                               1,
                               ['CS3241'],
                               ['CS3241:LEC'],
                               dry_run=True)

    def test_year_string_aliases(self):
        for year in ['2022-2023', '20222023', '2022/2023',
                     '22-23', '2223', '22/23',
                     '2023-2024', '2021-2022']:
            parse_and_generate_url(year,
                                   1,
                                   ['CS3241'],
                                   ['CS3241:LEC'],
                                   dry_run=True)

    def test_year_number_aliases(self):
        for year in [20222023, 2223, 20232024, 2324]:
            parse_and_generate_url(year,
                                   1,
                                   ['CS3241'],
                                   ['CS3241:LEC'],
                                   dry_run=True)

    def test_semester_aliases(self):
        for semester in [1, 2, "1", "2"]:
            parse_and_generate_url('2022-2023',
                                   semester,
                                   ['CS3241'],
                                   ['CS3241:LEC'],
                                   dry_run=True)

    def test_course_format(self):
        for course in ['cs3241', 'cS3241', 'Cs3241', 'Pls8001',
                       'cs1101S', 'laj4205hm']:
            parse_and_generate_url('2022-2023',
                                   1,
                                   [course],
                                   [],
                                   dry_run=True)

    def test_whitelist_format(self):
        for whitelist in ['cs3241:lec', 'cs3241:lec,rec,tut']:
            parse_and_generate_url('2022-2023',
                                   1,
                                   ['CS3241'],
                                   [whitelist],
                                   dry_run=True)

    def test_invalid_year(self):
        with self.assertRaises(ValueError):
            parse_and_generate_url('123456789',
                                   1,
                                   ['CS3241'],
                                   [],
                                   dry_run=True)

    def test_invalid_year_letters(self):
        with self.assertRaises(ValueError):
            parse_and_generate_url('y22/23',
                                   1,
                                   ['CS3241'],
                                   [],
                                   dry_run=True)

    def test_empty_year(self):
        with self.assertRaises(ValueError):
            parse_and_generate_url('',
                                   1,
                                   ['CS3241'],
                                   [],
                                   dry_run=True)

    def test_bad_semester_0(self):
        with self.assertRaises(ValueError):
            parse_and_generate_url('2022-2023',
                                   0,
                                   ['CS3241'],
                                   [],
                                   dry_run=True)

    def test_bad_semester_3(self):
        with self.assertRaises(ValueError):
            parse_and_generate_url('2022-2023',
                                   3,
                                   ['CS3241'],
                                   [],
                                   dry_run=True)

    def test_empty_semester(self):
        with self.assertRaises(ValueError):
            parse_and_generate_url('2022-2023',
                                   '',
                                   ['CS3241'],
                                   [],
                                   dry_run=True)

    # Querying the API is essential to determine if a course code is valid.
    # def test_bad_course_code(self):
    #     with self.assertRaises(ValueError):
    #         parse_and_generate_url('2022-2023',
    #                                '1',
    #                                ['acs09okc'],
    #                                [],
    #                                dry_run=True)

    # def test_empty_course_code(self):
    #     with self.assertRaises(ValueError):
    #         parse_and_generate_url('2022-2023',
    #                                '1',
    #                                [''],
    #                                [],
    #                                dry_run=True)

    def test_bad_whitelist(self):
        with self.assertRaises(ValueError):
            parse_and_generate_url('2022-2023',
                                   '1',
                                   ['CS3241'],
                                   ['asaoisc@aaiw'],
                                   dry_run=True)

    def test_misformatted_whitelist(self):
        with self.assertRaises(ValueError):
            parse_and_generate_url('2022-2023',
                                   '1',
                                   ['CS3241'],
                                   # Fails because we are very strict here?
                                   # Change if implementation changes
                                   ['CS2100: REC, LEC'],
                                   dry_run=True)

    def test_empty_whitelist(self):
        with self.assertRaises(ValueError):
            parse_and_generate_url('2022-2023',
                                   '1',
                                   ['CS3241'],
                                   [''],
                                   dry_run=True)

    def test_multiple_courses(self):
        parse_and_generate_url('2022-2023',
                               '1',
                               ['CS3241', 'CS3230', 'CS1101S'],
                               [],
                               dry_run=True)


    def test_multiple_whitelists(self):
        parse_and_generate_url('2022-2023',
                               '1',
                               ['CS3241', 'CS3230', 'CS1101S'],
                               ['CS2100:REC', 'CS2040S:TUT,LEC'],
                               dry_run=True)





if __name__ == '__main__':
    unittest.main()
