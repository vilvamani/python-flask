import unittest
from run import app

class BasicTests(unittest.TestCase):

    def test_main_page(self):
        response = app.test_client().get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
