import os

from pytest import fixture

from http_api import application


@fixture
def client():
    return application.test_client()


def test_sum_even_numbers_api(client):
    dirname = os.path.dirname(__file__)
    with open(f"{dirname}/numbers.txt", "rb") as file:
        response = client.post(
            "/sum_even_numbers",
            data=file.read(),
            headers={"Content-Type": "text/plain"},
        )
        assert response.status_code == 201
        assert "token" in response.json
