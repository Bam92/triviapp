import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category, database_name

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_user = "postgres"
        self.database_password = "postgres@psql"
        self.database_host = "localhost:5432"
        self.database_name = "trivia_test"

        # print("---------------ABEL")

        print(self.database_user) # unable to get this
        # print("---------------ABEL")

        # self.database_path = "postgresql://{}:{}@{}/{}".format(
        #     self.database_user, self.database_password, self.database_host, self.database_name
        # )
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        # setup_db(self.app, self.database_path)
# database_path = "postgresql://{}:{}@{}/{}".format(
#     database_user, database_password, database_host, database_name
# )
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            # self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_given_behavior(self):
        """Test _____________ """
        res = self.client().get('/questions')

        self.assertEqual(res.status_code, 200)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()