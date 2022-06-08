'''
Tests for jwt flask app.
'''
import os
import json
import pytest
import app


SECRET   = os.environ['SECRET']
TOKEN_EP = os.environ['EXECUTIVE_PRODUCER']
TOKEN_CD = os.environ['CASTING_DIRECTOR']
TOKEN_CA = os.environ['CASTING_ASSISTANT']


@pytest.fixture
def client():
    os.environ['JWT_SECRET'] = SECRET
    app.app.config['TESTING'] = True
    client = app.app.test_client()

    yield client


# Success test


def test_get_actors_success(client):
    headers = {'Authorization':  f'Bearer {TOKEN_EP}'}
    response = client.get('/actors', headers=headers)
    assert response.status_code in (200, 404)


def test_post_actors_success(client):
    body = {'name': 'actor1',
            'age': 25,
            'gender': 'M'}
    headers = {'Authorization':  f'Bearer {TOKEN_EP}'}
    response = client.post('/actors',
                           data=json.dumps(body),
                           content_type='application/json',
                           headers=headers)
    assert response.status_code == 200
    assert response.json['actors']['name'] == 'actor1'


def test_update_actors_success(client):
    body = {'name': 'actor3',
            'age': 28,
            'gender': 'M'}
    headers = {'Authorization':  f'Bearer {TOKEN_EP}'}
    response = client.patch('/actors/1',
                            data=json.dumps(body),
                            content_type='application/json',
                            headers=headers)
    assert response.status_code == 200
    assert response.json['actors']['name'] == 'actor3'


def test_delete_actors_success(client):
    headers = {'Authorization':  f'Bearer {TOKEN_EP}'}
    response = client.delete('/actors/1', headers=headers)
    assert response.status_code == 200
    assert response.json['actors'] == '1'


def test_get_movies_success(client):
    headers = {'Authorization':  f'Bearer {TOKEN_EP}'}
    response = client.get('/movies', headers=headers)
    assert response.status_code in (200, 404)


def test_post_movies_success(client):
    body = {'title': 'movie1',
            'release_date': '2019-12-11'}
    headers = {'Authorization':  f'Bearer {TOKEN_EP}'}
    response = client.post('/movies',
                           data=json.dumps(body),
                           content_type='application/json',
                           headers=headers)
    assert response.status_code == 200
    assert response.json['movies']['title'] == 'movie1'


def test_update_movies_success(client):
    body = {'title': 'movie2',
            'release_date': '2019-11-11'}
    headers = {'Authorization':  f'Bearer {TOKEN_EP}'}
    response = client.patch('/movies/1',
                            data=json.dumps(body),
                            content_type='application/json',
                            headers=headers)
    assert response.status_code == 200
    assert response.json['movies']['title'] == 'movie2'


def test_delete_movies_success(client):
    headers = {'Authorization':  f'Bearer {TOKEN_EP}'}
    response = client.delete('/movies/1', headers=headers)
    assert response.status_code == 200
    assert response.json['movies'] == '1'


# Error test
def test_get_actors_error(client):
    response = client.get('/actors')
    assert response.status_code == 401


def test_post_actors_error(client):
    body = {'a': 'actor1',
            'b': 25,
            'c': 'M'}
    headers = {'Authorization':  f'Bearer {TOKEN_EP}'}
    response = client.post('/actors',
                           data=json.dumps(body),
                           content_type='application/json',
                           headers=headers)
    assert response.status_code == 422


def test_update_actors_error(client):
    body = {'a': 'actor1',
            'b': 25,
            'c': 'M'}
    headers = {'Authorization':  f'Bearer {TOKEN_EP}'}
    response = client.patch('/actors/1',
                            data=json.dumps(body),
                            content_type='application/json',
                            headers=headers)
    assert response.status_code == 422


def test_delete_actors_error(client):
    headers = {'Authorization':  f'Bearer {TOKEN_EP}'}
    response = client.delete('/actors/100', headers=headers)
    assert response.status_code == 404


def test_get_movies_error(client):
    response = client.get('/movies')
    assert response.status_code == 401


def test_post_movies_error(client):
    body = {'a': 'movie1',
            'b': '2019-12-11'}
    headers = {'Authorization':  f'Bearer {TOKEN_EP}'}
    response = client.post('/movies',
                           data=json.dumps(body),
                           content_type='application/json',
                           headers=headers)
    assert response.status_code == 422


def test_update_movies_error(client):
    body = {'a': 'movie2',
            'b': '2000-11-12'}
    headers = {'Authorization':  f'Bearer {TOKEN_EP}'}
    response = client.patch('/movies/1',
                            data=json.dumps(body),
                            content_type='application/json',
                            headers=headers)
    assert response.status_code == 422


def test_delete_movies_error(client):
    headers = {'Authorization':  f'Bearer {TOKEN_EP}'}
    response = client.delete('/movies/100', headers=headers)
    assert response.status_code == 404


# Auth test
# Test for Casting Assistant
def test_get_actors_ca_success(client):
    headers = {'Authorization':  f'Bearer {TOKEN_CA}'}
    response = client.get('/actors', headers=headers)
    assert response.status_code in (200, 404)


def test_post_actors_ca_error(client):
    body = {'name': 'actor1',
            'age': 25,
            'gender': 'M'}
    headers = {'Authorization':  f'Bearer {TOKEN_CA}'}
    response = client.post('/actors',
                           data=json.dumps(body),
                           content_type='application/json',
                           headers=headers)
    assert response.status_code == 401


# Test for Casting Director
def test_post_actors_cd_success(client):
    body = {'name': 'actor1',
            'age': 25,
            'gender': 'M'}
    headers = {'Authorization':  f'Bearer {TOKEN_CD}'}
    response = client.post('/actors',
                           data=json.dumps(body),
                           content_type='application/json',
                           headers=headers)
    assert response.status_code == 200
    assert response.json['actors']['name'] == 'actor1'


def test_post_movies_cd_error(client):
    body = {'title': 'movie1',
            'release_date': '2019-12-11'}
    headers = {'Authorization':  f'Bearer {TOKEN_CD}'}
    response = client.post('/movies',
                           data=json.dumps(body),
                           content_type='application/json',
                           headers=headers)
    assert response.status_code == 401


# Test for Executive Producer
def test_post_movies_ep_success(client):
    body = {'title': 'movie1',
            'release_date': '2019-12-11'}
    headers = {'Authorization':  f'Bearer {TOKEN_EP}'}
    response = client.post('/movies',
                           data=json.dumps(body),
                           content_type='application/json',
                           headers=headers)
    assert response.status_code == 200
    assert response.json['movies']['title'] == 'movie1'


def test_delete_movies_ep_success(client):
    headers = {'Authorization':  f'Bearer {TOKEN_EP}'}
    response = client.delete('/movies/1', headers=headers)
    assert response.status_code in (200, 404)
