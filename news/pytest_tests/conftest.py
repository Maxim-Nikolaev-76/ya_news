from datetime import datetime, timedelta
import pytest
from django.urls import reverse
from django.test.client import Client
from django.utils import timezone
from news.models import News, Comment
from yanews import settings


COMMENT_TEXT = 'Комментарий'


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
        title='Новость',
        text='Текст новости',
    )
    return news


@pytest.fixture
def news_id(news):
    return (news.pk,)


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        text=COMMENT_TEXT,
        author=author
    )
    return comment


@pytest.fixture
def comment_id(comment):
    return comment.pk


@pytest.fixture
def all_news():
    today = datetime.today()
    all_news = News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Текст новости',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )
    return all_news


@pytest.fixture
def all_comments(author, news):
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'{COMMENT_TEXT} {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
    return comment


@pytest.fixture
def form_data():
    return {'text': 'Новый комментарий'}


@pytest.fixture
def detai_url(news_id):
    return reverse('news:detail', args=news_id)


@pytest.fixture
def delete_url(comment_id):
    return reverse('news:delete', args=(comment_id,))


@pytest.fixture
def edit_url(comment_id):
    return reverse('news:edit', args=(comment_id,))
