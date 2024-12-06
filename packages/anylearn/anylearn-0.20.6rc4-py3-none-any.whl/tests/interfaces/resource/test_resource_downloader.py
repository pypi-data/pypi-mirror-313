import os
import responses
from requests import RequestException

from anylearn.interfaces.resource.resource_downloader import SyncResourceDownloader
from tests.base_test_case import BaseTestCase

class TestResourceDownloader(BaseTestCase):

    @responses.activate
    def test_run_sync_resource_downloader_ok(self):
        responses.add(responses.POST, url=self._url("resource/compression"),
                        match_querystring=True,
                        json={'data': "COMP123"},
                        status=200)
        responses.add(responses.GET, url=self._url("resource/compression?file_id=FILE001&compression_id=COMP123"),
                            match_querystring=True,
                            json=[{'id': "COMP123", 'state': 2}],
                            status=200)
        downloader = SyncResourceDownloader()
        file_name = "test_sync_download.zip"
        headers = {'Content-Disposition': "attachment; filename=%s;" % file_name,}
        responses.add(responses.GET, url=self._url("resource/download?file_id=FILE001&compression_id=COMP123&token=TEST_TOKEN"),
                      match_querystring=True,
                      headers=headers,
                      status=200)
        res = downloader.run(resource_id="FILE001",
                             save_path="tests/")
        os.remove(f"tests/{file_name}")
        self.assertTrue(res)

    @responses.activate
    def test_run_sync_resource_downloader_500(self):
        downloader = SyncResourceDownloader()
        responses.add(responses.GET, url=self._url("resource/download?file_id=FILE001&token=TEST_TOKEN"),
                      status=500)
        with self.assertRaises(RequestException) as ctx:
            downloader.run(resource_id="FILE001",
                           save_path="/data/wtt")
        e = ctx.exception
        self.assertIsInstance(e, RequestException)
