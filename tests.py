import unittest
import json
import random
import string

from api import app, db

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


class BasicTests(unittest.TestCase):
    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False

        app.config['MONGODB_SETTINGS'] = {
            'db': 'users',
            'host': 'mongodb+srv://admin:XTiSq8Pm5MJsfmNA@cluster0-afsfl.mongodb.net/test?retryWrites=true&w=majority'
        }

        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    ###############
    #### tests ####
    ###############
    def main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_wrong_credentials(self):
        data = {
            "username": "test1234",
            "password": "asdsadsad"
        }
        response = self.app.post('/api/v1.0/auth/login', data=json.dumps(data),
                                 follow_redirects=True, content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_login(self):
        data = {
            "username": "lsd",
            "password": "chujkurwa"
        }
        response = self.app.post('/api/v1.0/auth/login', data=json.dumps(data),
                                 follow_redirects=True, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_login_without_parameters(self):
        response = self.app.post('/api/v1.0/auth/login',
                                 follow_redirects=True, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_login_without_arguments(self):
        data = {"username": "", "password": ""}

        response = self.app.post('/api/v1.0/auth/login', data=json.dumps(data),
                                 follow_redirects=True, content_type='application/json')
        self.assertEqual(response.status_code, 422)
        

    def test_register(self):
        data = {
            "username": randomString(10),
            "password": "chujkurwa",
            "email": f"{randomString(5)}@gmail.com"
        }

        response = self.app.post('/api/v1.0/auth/register', data=json.dumps(data),
                                 follow_redirects=True, content_type='application/json')
        self.assertEqual(response.json['message'], 'user successful created')
    
    def test_register_email_taken(self):
        data = {
            "username": randomString(10),
            "password": "chujkurwa",
            "email": "twojastara@gmail.com"
        }

        response = self.app.post('/api/v1.0/auth/register', data=json.dumps(data),
                                 follow_redirects=True, content_type='application/json')
        self.assertEqual(response.json['message'], 'email taken')
    
    def test_register_user_exists(self):
        data = {
            "username": "lsd",
            "password": "chujkurwa",
            "email": "test@twojastara.com"
        }

        response = self.app.post('/api/v1.0/auth/register', data=json.dumps(data),
                                 follow_redirects=True, content_type='application/json')
        self.assertEqual(response.json['message'], 'user already exists')

    # def unique_username(self):
    #     pass

unittest.main(BasicTests())
