from django.urls import reverse, resolve
from django.test import TestCase
from ..views import board_topics
from .TestHelper import TestHelper


class BoardTopicsTests(TestCase):

    def create_url(self, board_id):
        reverse('board_topics', kwargs={'board_id': board_id})

    # django creates new db for testing each time so we need
    # to setup a entry for testing
    def setUp(self):
        TestHelper.create_board()
        self.success_url = reverse('board_topics', kwargs={'board_id': 1})
        self.success_resp = self.client.get(self.success_url)

    def test_view_status_code_200(self):
        response = self.client.get(self.success_url)
        self.assertEquals(response.status_code, 200)

    def test_view_status_code_404(self):
        url = reverse('board_topics', kwargs={'board_id': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_view_url_resolves(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func, board_topics)

    def test_view_contains_link_back_to_homepage(self):
        homepage_url = reverse('home')
        self.assertContains(self.success_resp, f'href="{homepage_url}"')

    def test_view_contains_link_to_topics(self):
        new_topic_url = reverse('new_topic', kwargs={'board_id': 1})
        self.assertContains(self.success_resp, f'href="{new_topic_url}"')