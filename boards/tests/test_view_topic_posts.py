from django.test import TestCase
from django.urls import resolve, reverse

from ..views import topic_posts
from .TestHelper import TestHelper


class TopicPostsTests(TestCase):
    def setUp(self):
        board = TestHelper.create_board()
        user = TestHelper.create_user()
        topic = TestHelper.create_topic(board, user)
        TestHelper.create_post(topic, user)
        url = reverse('topic_posts', kwargs={'board_id': board.id, 'topic_id': topic.id})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/boards/1/topics/1/')
        self.assertEquals(view.func, topic_posts)