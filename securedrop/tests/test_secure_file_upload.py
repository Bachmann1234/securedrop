import unittest
from flask import session, g, escape
from cStringIO import StringIO
from io import BytesIO
from mock import patch

import source
import test_setup

class TestSecureFileUpload(unittest.TestCase):

    def setUp(self):
        self.app = source.app
        self.client = self.app.test_client()
        test_setup.create_directories()
        test_setup.init_gpg()
        test_setup.init_db()

    def tearDown(self):
        test_setup.clean_root()

    @patch('request_that_secures_file_uploads.create_secure_file_stream')
    def test_custom_file_upload_stream_is_used(self, create_secure_file_stream):
        create_secure_file_stream.return_value = BytesIO()
        test_setup.new_codename(self.client, session)

        self.client.post('/submit', data=dict(
            msg="",
            fh=(StringIO('This is a test'), "filename"),
        ), follow_redirects=True)

        create_secure_file_stream.assert_any_call()
