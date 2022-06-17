from django.test import SimpleTestCase


# tests for static pages

class SimpleTest(SimpleTestCase):

    def test_home_page_status(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_operating_status_page_status(self):
        response = self.client.get('/operating_status/')
        self.assertEqual(response.status_code, 200)

    def test_tables_page_status(self):
        response = self.client.get('/tables/')
        self.assertEqual(response.status_code, 200)

    def test_requests_page_status(self):
        response = self.client.get('/requests/')
        self.assertEqual(response.status_code, 200)
