from doctest import testfile
import unittest
from urllib import response
from flask import current_app

from flaskr import create_app

class TriviaTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.appctx = self.app.app_context()
        self.appctx.push()

    def tearDown(self):
        self.appctx.pop()
        self.app = None
        self.appctx = None

    def test_app(self):
        assert self.app is not None
        assert current_app == self.app
    
    def test_given_behavior(self):
        """Test _____________ """
        res = self.client().get('/questions')

        self.assertEqual(res.status_code, 200)

    # Check for response 200
    def test_index(self):
        app = create_app()
        tester = app.test_client(self)
        response = tester.get("/categories")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

if __name__ == "__main__":
    unittest.main()
