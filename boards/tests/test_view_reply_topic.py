from django.test import TestCase
from django.urls import reverse, resolve

from .TestHelper import TestHelper
from ..views import reply_topic
from ..forms import PostForm
from ..models import Post


class ReplyTopicTestCase(TestCase):
    """
    Base test case to be used in all `reply_topic` view tests
    """
    def setUp(self):
        self.board = TestHelper.create_board()
        self.username = 'john'
        self.password = '12345'
        user = TestHelper.create_user(self.username, self.password)
        self.topic = TestHelper.create_topic(self.board, user)
        self.post = TestHelper.create_post(self.topic, user)
        self.url = reverse('reply_topic', kwargs={'board_id': self.board.id, 'topic_id': self.topic.id})


class LoginRequiredReplyTopicTests(ReplyTopicTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))


class ReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code_200(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_status_code_404(self):
        url = reverse('reply_topic', kwargs={'board_id': 99, 'topic_id': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_view_function(self):
        view = resolve('/boards/1/topics/1/reply/')
        self.assertEquals(view.func, reply_topic)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PostForm)

    def test_form_inputs(self):
        """
        The view must contain two inputs: csrf, message textarea
        """
        self.assertContains(self.response, '<input', 1)
        self.assertContains(self.response, '<textarea', 1)


class SuccessfulReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {'message': 'hello, world!'})

    def test_redirection(self):
        """
        A valid form submission should redirect the user
        """
        topic_posts_url = reverse('topic_posts', kwargs={'board_id': self.board.id, 'topic_id': self.topic.id})
        self.assertRedirects(self.response, topic_posts_url)

    def test_reply_created(self):
        """
        The total post count should be 2
        The one created in the `ReplyTopicTestCase` setUp
        and another created by the post data in this class
        """
        self.assertEquals(Post.objects.count(), 2)


class InvalidReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        """
        Submit an empty dictionary to the `reply_topic` view
        """
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        """
        An invalid form submission should return to the same page
        """
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)