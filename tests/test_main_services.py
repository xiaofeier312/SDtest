from app.main.services import SDData as SD
import unittest

class MainServicesTestCase(unittest.TestCase):
    def setUp(self):
        self.testStr = 'abc1'
        self.testList = ['zz','xx','3']
        self.testJson = '{"aa":1,"bb":"zb"}'
        self.sd = SD()

    def tearDown(self):
        pass

    def test_main_service_split_text_str(self):
        result_str = self.sd.split_text(self.testStr)
        self.assertIsInstance(result_str,list,'split_text didnt transfer to list')

    def test_main_service_split_text_json(self):
        result_str = self.sd.split_text(self.testJson)
        self.assertIsInstance(result_str,list,'split_text didnt transfer to list')

