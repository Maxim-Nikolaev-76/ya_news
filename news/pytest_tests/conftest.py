import pytest
from django.test.client import Client
# from django.utils import timezone
from news.models import News, Comment


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news(author):
    news = News.objects.create(
        title='Заголовок',
        text='Текст заметки',
    )
    return news


@pytest.fixture
def news_id(news):
    return (news.pk,)


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        text='Комментарий',
        author=author
    )
    return comment


@pytest.fixture
def comment_id(comment):
    return comment.pk
