import requests
import allure
from .data import ServiceURLs


class APIClient:
    @staticmethod
    @allure.step('Регистрация нового пользователя')
    def register_user(profile_info):
        return requests.post(ServiceURLs.USER_REGISTRATION, json=profile_info)

    @staticmethod
    @allure.step('Аутентификация пользователя')
    def login_user(email, password):
        return requests.post(ServiceURLs.USER_LOGIN, json={"email": email, "password": password})

    @staticmethod
    @allure.step('Удаление профиля пользователя')
    def delete_user(auth_token):
        headers = {"Authorization": auth_token}
        return requests.delete(ServiceURLs.USER_PROFILE, headers=headers)

    @staticmethod
    def place_order(items, auth_token=None):
        headers = {}
        if auth_token:
            clean_token = auth_token.replace("Bearer ", "")
            headers["Authorization"] = f"Bearer {clean_token}"
        payload = {"ingredients": items}
        return requests.post(ServiceURLs.ORDER_ENDPOINT, json=payload, headers=headers)