from django.urls import reverse, resolve
from django.test import TestCase
from ..views import home
from ..models import Board
from .TestHelper import TestHelper


class HomeTest(TestCase):

    def setUp(self):
        self.board = TestHelper.create_board()
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    # check to make sure the view function being used to
    # render the page is the home function in views
    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('board_topics', kwargs={'board_id': self.board.id})
        self.assertContains(self.response, f'href="{board_topics_url}"')

