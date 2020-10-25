from django.urls import reverse, resolve
from django.test import TestCase
from django.contrib.auth.forms import User

from ..views import signup
from ..forms import SignUpForm


class SignUpTests(TestCase):

    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)
        self.view = resolve('/signup/')

    def test_200_status(self):
        self.assertEquals(self.response.status_code, 200)

    def test_resolves_view(self):
        self.assertEquals(self.view.func, signup)

    def test_contains_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input type="text"', 1)
        self.assertContains(self.response, '<input type="email"', 1)
        self.assertContains(self.response, '<input type="password"', 2)


class SuccessfulSignUpTest(TestCase):

    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'testuser',
            'email': 'testuser@email.com',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')

    def test_redirection(self):
        """
        A valid form submission should redirect the user to the home page
        """
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authenticated(self):
        """
        Create a new request to an arbitrary page.
        The resulting response should now have a `user` to its context,
        after a successful sign up.
        """
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSignUpTests(TestCase):

    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})

    def test_status_code(self):
        """
        An invalid form submission should return to the same page
        """
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_failed_user_creation(self):
        self.assertFalse(User.objects.exists())