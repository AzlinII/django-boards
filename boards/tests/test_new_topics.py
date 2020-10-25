from django.urls import reverse, resolve
from django.test import TestCase
from django.contrib.auth.models import User
from .TestHelper import TestHelper
from ..views import new_topic
from ..models import Topic, Post
from ..forms import NewTopicForm

class NewTopicTest(TestCase):

    def setUp(self):
        TestHelper.create_board()
        self.url = reverse('new_topic', kwargs={'board_id': 1})
        self.response = self.client.get(self.url)
        User.objects.create_user(username='test', email='test@test.com', password='123')

    def test_view_status_code_200(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_status_code_404(self):
        url = reverse('new_topic', kwargs={'board_id': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_view_url_resolves(self):
        view = resolve('/boards/1/new/')
        self.assertEquals(view.func, new_topic)

    def test_view_contains_link_back_to_board_topics(self):
        board_topics_url = reverse('board_topics', kwargs={'board_id': 1})
        self.assertContains(self.response, f'href="{board_topics_url}"')

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_valid_post(self):
        data = {
            'subject': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        self.client.post(self.url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_invalid_post(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        response = self.client.post(self.url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_invalid_post_empty_values(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)

