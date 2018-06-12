from app.main.services import SDProjectData as SD
import unittest
from app import db

class MainServicesTestCase(unittest.TestCase):
    def setUp(self):
        self.testStr = 'abc1Str'
        self.testList = ['zzlist','xx','3']
        self.testJson = '{"aaJson":1,"bb":"zb"}'
        self.sd = SD()

    def tearDown(self):
        db.session.remove()

    def test_main_service_split_text_str(self):
        result_str = self.sd.split_text(self.testStr)
        self.assertIsInstance(result_str,list,'split_text not transfer to list')

    def test_main_service_split_text_json(self):
        result_str = self.sd.split_text(self.testJson)
        self.assertIsInstance(result_str,list,'split_text not transfer to list')

    def test_main_service_split_text_list(self):
        result_str = self.sd.split_text(self.testList)
        self.assertIsInstance(result_str,list,'split_text not transfer to list')

    def test_main_service_get_parameters_list(self):
        result = self.sd.get_parameters_list(1)
        self.assertIsInstance(result,list,'return list')
        self.assertIn('705981',result, 'return 705981 not in list')
