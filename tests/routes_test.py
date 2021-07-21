import unittest, sys

sys.path.append('../Codegram-website') # imports python file from parent directory
from main import app #imports flask app object

class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        self.app = app.test_client()

    ###############
    #### tests ####
    ###############

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    def test_login(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200) 
    
    def test_register(self):
        response = self.app.get('register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()