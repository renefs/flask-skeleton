from app.tests import BaseTestCase
from flask import url_for


class Index(BaseTestCase):
    def test_index(self):
        response = self.client.get(url_for('common.index'))
        self.assertEqual(response.status_code, 200)
