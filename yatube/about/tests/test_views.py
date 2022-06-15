from django.test import Client, TestCase
from django.urls import reverse


class StaticViewsTests(TestCase):
    url_name_and_templates_dict = {
        'about:author': 'about/author.html',
        'about:tech': 'about/tech.html'
    }

    def setUp(self):
        self.guest_client = Client()

    def test_about_page_accessible_by_name(self):
        """URL, генерируемый при помощи имён в namespace about, доступен."""
        for address in self.url_name_and_templates_dict.keys():
            with self.subTest(address=address):
                response = self.guest_client.get(reverse(address))
                self.assertEqual(response.status_code, 200)

    def test_about_page_uses_correct_template(self):
        """При запросе к about применяются соответствующие шаблоны"""
        for address, template in self.url_name_and_templates_dict.items():
            with self.subTest(address=address):
                response = self.guest_client.get(reverse(address))
                self.assertTemplateUsed(response, template)
