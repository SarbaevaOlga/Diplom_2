import pytest
import requests
from api.data import create_user_data, ServiceURLs
from api.api_client import APIClient


@pytest.fixture(scope="function")
def existing_user_setup():
    user_profile = create_user_data()
    APIClient.register_user(user_profile)

    yield user_profile

    auth_result = APIClient.login_user(user_profile["email"], user_profile["password"])
    token = auth_result.json()["accessToken"]

    APIClient.delete_user(token)


@pytest.fixture(scope="function")
def test_data_cleanup():
    user_info = {}

    yield user_info

    if user_info.get("email") and user_info.get("password"):
        auth_result = APIClient.login_user(user_info["email"], user_info["password"])
        token = auth_result.json()["accessToken"]
        APIClient.delete_user(token)


@pytest.fixture(scope="session")
def get_available_items():
    response = requests.get(ServiceURLs.ITEMS_LIST)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    return [item["_id"] for item in data["data"][:2]]