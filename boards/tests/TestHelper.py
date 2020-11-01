from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Board, Topic, Post


class TestHelper(TestCase):

    @staticmethod
    def create_board():
        return Board.objects.create(name='Test Board', description='Testing Board')

    @staticmethod
    def create_user(username='john', password='123'):
        return User.objects.create_user(username=username, email='john@doe.com', password=password)

    @staticmethod
    def create_topic(board, user):
        return Topic.objects.create(subject='Hello, world', board=board, starter=user)

    @staticmethod
    def create_post(topic, user):
        Post.objects.create(message='Lorem ipsum dolor sit amet', topic=topic, created_by=user)
