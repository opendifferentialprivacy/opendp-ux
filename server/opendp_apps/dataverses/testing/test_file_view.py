from unittest import skip
import requests_mock

from django.test import TestCase

from opendp_apps.dataverses.dataverse_manifest_params import DataverseManifestParams
from opendp_apps.dataverses.models import ManifestTestParams
from opendp_apps.dataverses.testing import schema_test_data
from opendp_apps.dataverses.testing.test_endpoints import BaseEndpointTest
from opendp_apps.model_helpers.msg_util import msgt


# TODO: split this into endpoint and view tests
class FileViewGetTest(BaseEndpointTest):

    fixtures = ['test_dataverses_01.json',
                'test_manifest_params_04.json',
                'test_opendp_users_01.json']

    @skip("Mocking issues with schema here")
    @requests_mock.Mocker()
    def test_00_list_successful(self, req_mocker):
        """(00) test_list_successful"""
        msgt(self.test_00_list_successful.__doc__)
        self.set_mock_requests(req_mocker)

        response = self.client.get('/api/dv-file/',
                                   data={'handoff_id': '9e7e5506-dd1a-4979-a2c1-ec6e59e4769c',
                                         'user_id': '6c4986b1-e90d-48a2-98d5-3a37da1fd331'})
        print("RESPONSE: ", response.json())
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json().get('dv_installation'), 1)

    @requests_mock.Mocker()
    def test_10_successful_get(self, req_mocker):
        """(10) test_successful_creation"""
        msgt(self.test_10_successful_get.__doc__)
        self.set_mock_requests(req_mocker)

        # From fixture file: "test_manifest_params_04.json"
        tparams = ManifestTestParams.objects.get(object_id='4bcad631-ce7c-475e-a569-29e71ee0b2ee')
        handoff_req = tparams.make_test_handoff_object()
        self.assertTrue(handoff_req.success is True)
        handoff_obj = handoff_req.data

        # The Mock url is for when the applications calls "Dataverse" to retrieve JSON-LD metadata
        #
        mock_url = ('http://127.0.0.1:8000/dv-mock-api/api/v1/datasets/export'
                    '?exporter=schema.org&persistentId=doi:10.7910/DVN/PUXVDH'
                    '&User-Agent=pydataverse&key=shoefly-dont-bother-m3')
        req_mocker.get(mock_url, json=tparams.schema_org_content)

        response = self.client.get('/api/dv-file/',
                                   data={'handoff_id': handoff_obj.object_id,
                                         'user_id': '6c4986b1-e90d-48a2-98d5-3a37da1fd331'},
                                   content_type='application/json')
        #print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('success'), True)
        self.assertTrue('dataset_schema_info' in response.json().get('data', {}))
        self.assertTrue('file_schema_info' in response.json().get('data', {}))

    @requests_mock.Mocker()
    def test_15_unsuccessful_get(self, req_mocker):
        """(15) Schema.org retrieved but file specific info is not found!"""
        msgt(self.test_15_unsuccessful_get.__doc__)

        # From fixture file: "test_manifest_params_04.json"
        tparams = ManifestTestParams.objects.get(object_id='4bcad631-ce7c-475e-a569-29e71ee0b2ee')
        handoff_req = tparams.make_test_handoff_object()
        self.assertTrue(handoff_req.success is True)
        handoff_obj = handoff_req.data

        # The Mock url is for when the applications calls "Dataverse" to retrieve JSON-LD metadata
        #
        mock_url = ('http://127.0.0.1:8000/dv-mock-api/api/v1/datasets/export'
                    '?exporter=schema.org&persistentId=doi:10.7910/DVN/PUXVDH'
                    '&User-Agent=pydataverse&key=shoefly-dont-bother-m3')

        # Changing the schema org reponse so that it doesn't contain any file info
        schema_content = tparams.schema_org_content
        schema_content['distribution'] = [] # no file info

        req_mocker.get(mock_url, json=schema_content)

        response = self.client.get('/api/dv-file/',
                                   data={'handoff_id': handoff_obj.object_id,
                                         'user_id': '6c4986b1-e90d-48a2-98d5-3a37da1fd331'},
                                   content_type='application/json')
        #print(response.json())
        print('response.status_code', response.status_code)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('success'), False)
        self.assertTrue('message' in response.json())

    def test_20_schema_info_parsing(self):
        """Retrieve the correct dataset from schema info, using File Ids"""
        msgt(self.test_20_schema_info_parsing.__doc__)

        # Schema contains file info, when file Id is an int
        #
        file_resp = DataverseManifestParams.get_file_specific_schema_info( \
            schema_test_data.schema_info_01,
            file_id=schema_test_data.schema_info_01_file_id,
            file_persistent_id=schema_test_data.schema_info_01_file_pid)

        self.assertTrue(file_resp.success is True)
        self.assertTrue('contentUrl' in file_resp.data)

        self.assertTrue(file_resp.data['contentUrl'].endswith(str(schema_test_data.schema_info_01_file_id)))

        # Schema contains file info, when file Id is a string
        #
        file_resp = DataverseManifestParams.get_file_specific_schema_info(\
                                            schema_test_data.schema_info_01,
                                            file_id=str(schema_test_data.schema_info_01_file_id),
                                            file_persistent_id=schema_test_data.schema_info_01_file_pid)

        self.assertTrue(file_resp.success is True)
        self.assertTrue('contentUrl' in file_resp.data)
        self.assertTrue(file_resp.data['contentUrl'].endswith(str(schema_test_data.schema_info_01_file_id)))

    def test_30_schema_info_parsing_bad_id(self):
        """Bad File Id used to retrieve data from schema info"""
        msgt(self.test_30_schema_info_parsing_bad_id.__doc__)

        # Bad File Id, as a string, used to retrieve data from schema info
        bad_file_id = '63'
        file_resp = DataverseManifestParams.get_file_specific_schema_info(\
                                            schema_test_data.schema_info_01,
                                            file_id=bad_file_id,
                                            file_persistent_id=schema_test_data.schema_info_01_file_pid)
        self.assertTrue(file_resp.success is False)
        self.assertTrue(file_resp.message.find(bad_file_id) > -1)


        # Schema does NOT contain file info, bad id as int
        #
        bad_file_id = 99999
        file_resp = DataverseManifestParams.get_file_specific_schema_info(\
                                            schema_test_data.schema_info_01,
                                            file_id=bad_file_id,
                                            file_persistent_id=schema_test_data.schema_info_01_file_pid)
        self.assertTrue(file_resp.success is False)
        self.assertTrue(file_resp.message.find(str(bad_file_id)) > -1)

    def test_40_schema_info_parsing(self):
        """Retrieve the correct dataset from schema info, uses DOIs"""
        msgt(self.test_40_schema_info_parsing.__doc__)

        # Schema contains file info, when file Id is an int
        #
        file_resp = DataverseManifestParams.get_file_specific_schema_info( \
            schema_test_data.schema_info_02,
            file_id=schema_test_data.schema_info_02_file_id,
            file_persistent_id=schema_test_data.schema_info_02_file_pid)

        self.assertTrue(file_resp.success is True)
        print(file_resp.data)
        self.assertTrue('contentUrl' in file_resp.data)
        self.assertTrue(file_resp.data['identifier'].endswith(schema_test_data.schema_info_02_file_pid))
