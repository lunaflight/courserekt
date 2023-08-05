import unittest
from contextlib import closing
from src.web.app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        # Create a test client to make requests to the app
        self.app = app.test_client()
        app.testing = True

    def tearDown(self):
        # Clean up any resources after each test case is run
        pass

    def test_homepage(self):
        # Test the homepage route
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_form_submission(self):
        data = {
            'year': '2223',
            'semester': '2',
            'type': 'gd'
        }
        response = self.app.post('/', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_serve_pdf(self):
        with closing(self.app.get('/pdfs/2324/1/ug/round_1.pdf')) as response:
            self.assertEqual(response.status_code, 200)

    def test_invalid_route(self):
        response = self.app.get('/invalid_route')
        self.assertEqual(response.status_code, 404)

    def test_invalid_pdf(self):
        response = self.app.get('/pdfs/2223/3/ug/round_0.pdf')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
