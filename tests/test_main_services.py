from app.main.services import SDProjectData as SD
import unittest

class MainServicesTestCase(unittest.TestCase):
    def setUp(self):
        self.testStr = 'abc1Str'
        self.testList = ['zzlist','xx','3']
        self.testJson = '{"aaJson":1,"bb":"zb"}'
        self.sd = SD()

    def tearDown(self):
        pass

    def test_main_service_split_text_str(self):
        result_str = self.sd.split_text(self.testStr)
        self.assertIsInstance(result_str,list,'split_text didnt transfer to list')

    def test_main_service_split_text_json(self):
        result_str = self.sd.split_text(self.testJson)
        self.assertIsInstance(result_str,list,'split_text didnt transfer to list')

    def test_main_service_split_text_list(self):
        result_str = self.sd.split_text(self.testList)
        self.assertIsInstance(result_str,list,'split_text didnt transfer to list')