# from datetime import datetime, timedelta

# def split_date_interval(start_date, end_date):
#     # Convert input strings to datetime objects
#     start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
#     end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
#     end_datetime = end_datetime+ timedelta(days=1)


#     # Calculate the number of 7-day intervals between the two dates
#     num_weeks = int((end_datetime - start_datetime).days / 7)

#     # Create a list of dates by adding 7 days to the start date for each interval
#     date_list = []
#     for i in range(num_weeks + 1):
#         date_list.append((start_datetime + timedelta(weeks=i)).strftime('%Y-%m-%d'))
#     date_list.append(end_datetime.strftime('%Y-%m-%d'))

#     return date_list


# print(split_date_interval('2022-02-02', '2022-02-20'))

from server import app
import unittest
import json

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_status_code_correct_request(self):
        response = self.app.get('/neos?start_date=2022-02-02&end_date=2022-02-02')
        self.assertEqual(response.status_code, 200)
    
    def test_status_code_no_params(self):
        response = self.app.get('/neos')
        self.assertEqual(response.status_code, 400)
    
    def test_status_code_invalid_param_formats(self):
        response = self.app.get('/neos?start_date=dadsa&end_date=2022-02-02')
        self.assertEqual(response.status_code, 400)

        response = self.app.get('/neos?start_date=2022-02-02&end_date=dasdsa')
        self.assertEqual(response.status_code, 400)
    
    def test_status_code_invalid_interval(self):
        response = self.app.get('/neos?start_date=2022-02-02&end_date=2022-01-02')
        self.assertEqual(response.status_code, 400)
    
    def test_correct_data_returned(self):
        response = self.app.get('/neos?start_date=2000-02-02&end_date=2000-02-10')
        returned_data = json.loads(response.text)
        with open('test_data.json', 'r') as file:
            compare_data = json.loads(file.read())
        
        #this might fail if two different objects have the same distance
        returned_data = sorted(returned_data, key=lambda x: float(x['distance'].replace(' km', '')))
        compare_data = sorted(compare_data, key=lambda x: float(x['distance'].replace(' km', '')))
        self.assertEqual(returned_data, compare_data)
        




if __name__ == '__main__':
    unittest.main()