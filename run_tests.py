

from server import app
import unittest
import json
import os

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def test_api_key_present(self):
        api_key = os.environ.get("NASA_API_KEY")
        assert api_key != None

    def test_status_code_correct_request(self):
        response = self.app.get('/objects?start_date=2022-02-02&end_date=2022-02-02')
        self.assertEqual(response.status_code, 200)
    
    def test_status_code_no_params(self):
        response = self.app.get('/objects')
        self.assertEqual(response.status_code, 400)
    
    def test_status_code_invalid_param_formats(self):
        response = self.app.get('/objects?start_date=dadsa&end_date=2022-02-02')
        self.assertEqual(response.status_code, 400)

        response = self.app.get('/objects?start_date=2022-02-02&end_date=dasdsa')
        self.assertEqual(response.status_code, 400)
    
    def test_status_code_invalid_interval(self):
        response = self.app.get('/objects?start_date=2022-02-02&end_date=2022-01-02')
        self.assertEqual(response.status_code, 400)
    
    def test_correct_data_returned(self):
        response = self.app.get('/objects?start_date=2000-02-02&end_date=2000-02-10')
        returned_data = json.loads(response.text)
        with open('test_data.json', 'r') as file:
            compare_data = json.loads(file.read())
        self.assertEqual(returned_data, compare_data)
        



if __name__ == '__main__':
    unittest.main()