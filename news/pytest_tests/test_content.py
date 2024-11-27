import pytest
from django.urls import reverse
from yanews import settings
from news.forms import CommentForm


HOME_URL = reverse('news:home')


@pytest.mark.django_db
def test_news_count(client, all_news):
    response = client.get(HOME_URL)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, all_news):
    response = client.get(HOME_URL)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, news, all_comments, news_id):
    response = client.get(reverse('news:detail', args=news_id))
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


def test_anonymouse_client_has_no_form(client, news, news_id):
    response = client.get(reverse('news:detail', args=news_id))
    assert 'form' not in response.context


def test_authorized_client_has_form(author_client, news, news_id):
    response = author_client.get(reverse('news:detail', args=news_id))
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
