from http import HTTPStatus
from pytest_django.asserts import assertRedirects, assertFormError
from news.models import Comment
from news.forms import BAD_WORDS, WARNING
from .conftest import COMMENT_TEXT


def test_anonymous_client_cant_create_comment(
        client,
        news,
        detai_url,
        form_data
):
    client.post(
        detai_url,
        data=form_data
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_authorized_client_can_create_comment(
        author_client,
        author,
        news,
        detai_url,
        form_data
):
    response = author_client.post(
        detai_url,
        data=form_data
    )
    assertRedirects(response, f'{detai_url}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, news, detai_url):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(detai_url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comment_count = Comment.objects.count()
    assert comment_count == 0


def test_author_can_delete_comment(
        author_client,
        news,
        comment,
        delete_url,
        detai_url
):
    response = author_client.delete(delete_url)
    url_to_comments = detai_url + '#comments'
    assertRedirects(response, url_to_comments)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_not_author_cant_delete_comment(
        not_author_client,
        news,
        comment,
        delete_url
):
    response = not_author_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_author_can_edit_comment(
        author_client,
        news,
        comment,
        edit_url,
        form_data,
        detai_url,
):
    response = author_client.post(edit_url, data=form_data)
    url_to_comments = detai_url + '#comments'
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == form_data['text']


def test_not_author_cant_edit_comment(
        not_author_client,
        news,
        comment,
        edit_url,
        form_data,
):
    response = not_author_client.post(edit_url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == COMMENT_TEXT
