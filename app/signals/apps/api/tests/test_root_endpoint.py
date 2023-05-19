# SPDX-License-Identifier: MPL-2.0
# Copyright (C) 2019 - 2023 Gemeente Amsterdam
import os

from signals import __version__
from signals.test.utils import SignalsBaseApiTestCase

THIS_DIR = os.path.dirname(__file__)
SIGNALS_TEST_DIR = os.path.join(os.path.split(THIS_DIR)[0], '..', 'signals')


class TestAPIRoot(SignalsBaseApiTestCase):

    def test_http_header_api_version(self):
        response = self.client.get('/signals/v1/')
        self.assertEqual(response['X-API-Version'], __version__)
