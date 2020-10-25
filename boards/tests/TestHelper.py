from ..models import Board
from django.test import TestCase


class TestHelper(TestCase):

    @staticmethod
    def create_board():
        return Board.objects.create(name='Test Board', description='Testing Board')
