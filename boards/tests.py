# from django.urls import reverse, resolve
# from django.test import TestCase
# from .views import home, board_topics
# from .models import Board
#
#
# # Create your tests here.
#
# class HomeTest(TestCase):
#
#     def test_home_view_status_code(self):
#         url = reverse("home")
#         response = self.client.get(url)
#         self.assertEquals(response.status_code, 200)
#
#     # check to make sure the view function being used to
#     # render the page is the home function in views
#     def test_home_url_resolves_home_view(self):
#         view = resolve('/')
#         self.assertEquals(view.func, home)
#
#
# class BoardTopicsTests(TestCase):
#     # django creates new db for testing each time so we need
#     # to setup a entry for testing
#     def setUp(self):
#         Board.objects.create(name='Test Board', description='Testing Board')
#
#     def test_board_topics_view_success_status_code(self):
#         url = reverse("board_topics", kwargs={'board_id': 1})
#         response = self.client.get(url)
#         self.assertEquals(response.status_code, 200)
#
#     def test_board_topics_view_not_found_status_code(self):
#         url = reverse('board_topics', kwargs={'board_id': 99})
#         response = self.client.get(url)
#         self.assertEquals(response.status_code, 404)
#
#     def test_board_topics_url_resolves_board_topics_view(self):
#         view = resolve('/boards/1/')
#         self.assertEquals(view.func, board_topics)
#
