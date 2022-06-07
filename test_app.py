'''
Tests for jwt flask app.
'''
import os
import json
import pytest
import app


SECRET = 'TestSecret'
TOKEN_EP = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJFWXpNRVJGUWpKRFFUUkdOVE0zTXpKQ1JqQXpOakpETXpVd1EwRTVNamhHTmpjNU1qUkdNUSJ9.eyJpc3MiOiJodHRwczovL2Rldi1lcmJxdHI3aS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRkZDIzNWQ3YjNlZmIwY2QwYWYzODQ2IiwiYXVkIjoiY2FzdGluZ19hZ2VuY3kiLCJpYXQiOjE1NzkzNDczNzYsImV4cCI6MTU3OTQzMzc3NiwiYXpwIjoicXBnSUJzS01sVnczRVpZcG1PYWZ2MHdZaHFmd1RCZ04iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.whE9fmQ7hbEMvrFn0P5DG44RXZeBAGvXXYUsWwVGfcRr2wRIkT0hLnJh_EdTfLXjFgJy9_PzySDnPMAZqVdCjV-bBV_tfP0nBwqar3VBZr9itKDTu7t97c1pa4QxtBrZwb779T3GPN89XBRmwAam7lgMgwbj-HdzopfdFXN0frygi7UtY0L7EmUPfMRe9H87ZVUYYZHXITdpljRYiFw0C5P-RdHbal0OjpGaEulYPQ54WtRw9W-mR752jKxcR7hS6KbV0yshBzKiTrHy-nvfbFG0RHkuWFZpPOmm3K1BCUTVwrC2fxwLkwFmftyqoFQCO9ghw74UBi2KEeS-zBJSiA'
TOKEN_CD = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJFWXpNRVJGUWpKRFFUUkdOVE0zTXpKQ1JqQXpOakpETXpVd1EwRTVNamhHTmpjNU1qUkdNUSJ9.eyJpc3MiOiJodHRwczovL2Rldi1lcmJxdHI3aS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRkY2UwNjE3YjNlZmIwY2QwYWYzMzZhIiwiYXVkIjoiY2FzdGluZ19hZ2VuY3kiLCJpYXQiOjE1NzkzNDc1NTAsImV4cCI6MTU3OTQzMzk1MCwiYXpwIjoicXBnSUJzS01sVnczRVpZcG1PYWZ2MHdZaHFmd1RCZ04iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.GgigHEIF0gjRzqrY5f-QHe-l2UMRrtoAtrwqCLQAmI1FCd_m0OqsTerjehKyH5gX1BpcsCFLU4bMiC-yQp4DFET6NYYiuReTLD6fUOeU91Sfd4cplWw1Jgaseib9692NPqd3xJLAzw16Q5F9SEdHUtb4AlLAVU2z9Wv6UkmiO-smenAwEZBeuPxMF1AwzX0lhNSzST1n8MTqyWwHH4JaHGnQQ0tlfg24PZBWQsJYsuF1S6Hk7tUK_Lf-pd5dSGNPA7YdfnXzc2zqpBBvd_Db7k-5i3iYk8T6StS1Ixlio7x5xuIjT-r0a_obUDtexjuPHMUOouhtDxf6N3407F8yPQ'
TOKEN_CA = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJFWXpNRVJGUWpKRFFUUkdOVE0zTXpKQ1JqQXpOakpETXpVd1EwRTVNamhHTmpjNU1qUkdNUSJ9.eyJpc3MiOiJodHRwczovL2Rldi1lcmJxdHI3aS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRkN2UxOTAyOTkwNzcwZjJhMzI5Y2ZjIiwiYXVkIjoiY2FzdGluZ19hZ2VuY3kiLCJpYXQiOjE1NzkzNDc2NDcsImV4cCI6MTU3OTQzNDA0NywiYXpwIjoicXBnSUJzS01sVnczRVpZcG1PYWZ2MHdZaHFmd1RCZ04iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.IlfUZye5PnYcLUTCXGYvcqzihdrVfp70JCLCHszwbVJj7-uzymsWxCNG7-_20PYZAPb1YmBwsIoT8HISBmI4YIiUXeV_6WWrIyzrEePiZAQ48slO8mi0A2ONCYR0sOu19ji7oie8tvZNhlEXBk4m1uNkK2Q4J59UuiJmatJwhfaxDlcE-OaxUzp02IlXSyXMaK_T7ep07KT62HcsyTG3HzX61375dJI3GHmnMbnCNwxPnGFQUTLljQsox99XpXay7ivkGllOwzdoQ6RqvfuUmD8tpwxedCZyJ189VFm7-kIdBkohlklXnzPO4mEYw0o_1Od5Kra7kRXDNKNHgNWUPg'


@pytest.fixture
def client():
    os.environ['JWT_SECRET'] = SECRET
    app.APP.config['TESTING'] = True
    client = app.APP.test_client()

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
            'b': '2019-11-11'}
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