from pathlib import Path
import responses
from unittest import TestCase

from anylearn.config import AnylearnConfig
from .config import (
    test_host,
    test_username,
    test_password,
    test_workspace
)

class BaseTestCase(TestCase):
    @responses.activate
    def setUp(self):
        responses.add(responses.POST, url=self._url("user/login"),
                      json={
                          'id': "USER001",
                          'refresh_token': "TEST_REFRESH_TOKEN",
                          'token': "TEST_TOKEN",
                          'username': test_username
                      },
                      status=200)
        AnylearnConfig.init(
            cluster_address=test_host,
            username=test_username,
            password=test_password,
            workspace=test_workspace,
            disable_git=True,
        )

    def tearDown(self):
        AnylearnConfig.clear_workspace()

    def _url(self, route):
        return f"{test_host}/api/{route}"
