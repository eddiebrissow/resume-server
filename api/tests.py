import os

from rest_framework.test import APITestCase
from django.contrib.auth.models import User




class ResumeTestCase(APITestCase):

    def setUp(self):
        # self.client = APIClient()
        self.user = {"username": "test", "password": "test", "email": "1234@1234.com"}
        self.api_url = 'http://127.0.0.1:8000/api/v1/{}'
        self.oath_url = 'http://127.0.0.1:8000/{}'
        self.api_token = ''
        self.admin_user = User.objects.create_superuser('admin', 'admin@admin', 'admin')
        self.client_id = 'GfwHHKohhtSxPm5kB32QrOu075MdkLkfNBhusmM0'
        self.client_secret = 'ayfC03lLJwldQFU4oRmjTs7566FJrwUBLlU9KkxWSsrRlpPzsMPFmDPOhMXDELxhYFJB3BCaITskauVJTDKOxd' \
                             'lbsWXzfR68lJ86Gi9HYXa7dKO2qxui5veSStEucv90'
        self.files_folder = os.path.abspath('') + '/api/test_files/'
        self.test_files = ['ds.pdf', 'sbc.pdf']
        self.application = {
            'name': 'asdasdasd',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'client_type': 'confidential',
            'authorization_grant_type': 'password',
            'redirect_uris': ''
        }
        self.application_info = {
            'grant_type': 'password',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'username': 'admin',
            'password': 'admin'
        }



    def get_api_token(self):
        is_logged = self.client.login(username='admin', password='admin')
        if is_logged:
            self.client.post(self.oath_url.format('o/applications/register/'), self.application)
            token_response = self.client.post(self.oath_url.format('o/token/'), self.application_info)
            self.api_token = dict(token_response.json()).get('access_token')
        return self.api_token

    def get_credentials(self):
        self.get_api_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.api_token)

    def add_file(self, filename):
        with open(self.files_folder + filename, 'rb') as pdf_file:
            response = self.client.post(self.api_url.format('resumes/'),
                                        {
                                            'file': pdf_file
                                        })
            return response

    def update_file(self, filename, id):
        with open(self.files_folder + filename, 'rb') as pdf_file:
            response = self.client.put(self.api_url.format('resumes/' + str(id)),
                                       {
                                           'file': pdf_file
                                       })
            return response

    def test_add_user_and_login(self):
        print('Test Add User')
        response = self.client.post(self.api_url.format('users/'), self.user)
        is_logged = self.client.login(username='test', password='test')
        self.client.logout()
        assert response.status_code == 201 and is_logged

    def test_create_application(self):
        print('Create Application')
        assert (self.get_api_token())

    def test_create_resume(self):
        print('Test Create Resume')
        self.get_credentials()
        response = self.add_file(self.test_files[0])
        assert response.status_code == 201

    def test_update_resume(self):
        print('Test Update Resume')
        self.get_credentials()
        add_response = self.add_file(self.test_files[0])
        up_response = self.update_file(self.test_files[1], dict(add_response.json()).get('id'))
        assert up_response.status_code == 200

    def test_ordering_resumes(self):
        print('Test Ordering Resumes')
        self.get_credentials()
        [self.add_file(tf) for tf in self.test_files]
        response = self.client.get(self.api_url.format('resumes/?ordering=file'))
        reponse_dict = dict(response.json())
        if reponse_dict:
            count = reponse_dict.get('count')
            results = reponse_dict.get('results')
            value1 = 'ds' in results[0].get('file')
            value2 = 'sbc' in results[1].get('file')

        assert count == 2 and value1 and value2

    def test_filtering_resumes(self):
        print('Test Filtering Resumes')
        self.get_credentials()
        [self.add_file(tf) for tf in self.test_files]

        response = self.client.get(self.api_url.format('resumes/?file=sbc'))
        reponse_dict = dict(response.json())
        if reponse_dict:
            count = reponse_dict.get('count')
            results = reponse_dict.get('results')
            value = 'sbc' in results[0].get('file')

        assert count == 1 and value




