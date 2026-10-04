import pytest
from django.contrib.auth import get_user_model

def test_health(client):
    assert client.get("/health/").json() == {"status": "ok"}

@pytest.mark.django_db
def test_database():
    assert get_user_model().objects.count() == 0