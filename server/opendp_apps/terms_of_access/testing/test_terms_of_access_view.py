import requests_mock

from rest_framework.test import APIClient

from opendp_apps.dataverses.testing.test_endpoints import BaseEndpointTest
from opendp_apps.model_helpers.msg_util import msgt


@requests_mock.Mocker()
class TestTermsOfAccessView(BaseEndpointTest):

    client = APIClient()
    fixtures = ['test_dataverses_01.json',
                'test_manifest_params_04.json',
                'test_opendp_users_01.json',
                'test_terms_of_access_01.json']

    terms_of_access = {'name': 'Harvard Dataverse Terms of Access',
                       'active': True,
                       'description': 'an in-depth description',
                       'version': 0.0,
                       'notes': 'Harvard Dataverse TOA'}

    def test_10_list_successful(self, req_mocker):
        """(10) test_list_successful"""
        msgt(self.test_10_list_successful.__doc__)
        self.set_mock_requests(req_mocker)

        response = self.client.get('/api/terms-of-access/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json().get('results'), [self.terms_of_access])

    def test_20_get_successful(self, req_mocker):
        """(20) test_get_successful"""
        msgt(self.test_20_get_successful.__doc__)
        self.set_mock_requests(req_mocker)

        response = self.client.get('/api/terms-of-access/1/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json(), self.terms_of_access)

    def test_30_get_unsuccessful(self, req_mocker):
        """(30) test_get_unsuccessful"""
        msgt(self.test_30_get_unsuccessful.__doc__)
        self.set_mock_requests(req_mocker)

        # There is no TermsOfAccess with id=2
        response = self.client.get('/api/terms-of-access/2/')
        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.json(), {'detail': 'Not found.'})

