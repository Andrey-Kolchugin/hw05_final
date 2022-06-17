from http import HTTPStatus
from django.test import Client, TestCase


class StaticURLTests(TestCase):
    urls_and_templates_dict = {
        '/about/author/': 'about/author.html',
        '/about/tech/': 'about/tech.html'
    }

    def setUp(self):
        self.guest_client = Client()

    def test_about_url_exists_at_desired_location(self):
        """Проверка доступности адресов /about/."""
        for address in self.urls_and_templates_dict.keys():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_url_uses_correct_template(self):
        """Проверка шаблона для адресов /about/."""
        for address, template in self.urls_and_templates_dict.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)
