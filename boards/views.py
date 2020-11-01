from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Board, Post, Topic
from .forms import NewTopicForm


# Create your views here.
def home(request):
    """
    renders the home view - ''
    :param request: request object
    :return:
    """
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})


def board_topics(request, board_id):
    """
    renders the board_topics view - '/board/{board_id}/'
    :param request: request object
    :param board_id: the board id
    :return:
    """
    board = get_object_or_404(Board, id=board_id)
    return render(request, 'topics.html', {'board': board})


@login_required
def new_topic(request, board_id):
    """
    renders the new_topic view - '/board/{board_id}/new/'
    :param request: request object
    :param board_id: the board id
    :return:
    """
    board = get_object_or_404(Board, id=board_id)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('board_topics', board_id=board.id)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


def topic_posts(request, board_id, topic_id):
    topic = get_object_or_404(Topic, board_id=board_id, id=topic_id)
    return render(request, 'topic_posts.html', {'topic': topic})