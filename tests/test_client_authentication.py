import pytest
import allure
from api.api_client import APIClient
from api.data import APIResponses, TestConfig


@allure.feature('Аутентификация пользователя')
class TestUserAuthentication:

    @allure.title('Успешная аутентификация зарегистрированного пользователя')
    def test_login_existing_user_success(self, existing_user_setup):
        user_info = existing_user_setup

        with allure.step('Выполнить запрос аутентификации'):
            result = APIClient.login_user(user_info["email"], user_info["password"])

        with allure.step('Проверить успешность входа'):
            assert result.status_code == 200
            assert result.json()["success"] == True
            assert result.json()["user"]["email"] == user_info["email"]

    @allure.title('Аутентификация с некорректным email')
    def test_login_fails_wrong_email(self, existing_user_setup):
        with allure.step('Использовать несуществующий email'):
            user_info = existing_user_setup
            wrong_email = TestConfig.INVALID_DATA

        with allure.step('Отправить запрос с неверным email'):
            result = APIClient.login_user(wrong_email, user_info["password"])

        with allure.step('Проверить ошибку аутентификации'):
            assert result.status_code == 401
            assert result.json() == APIResponses.LOGIN_FAILED

    @allure.title('Аутентификация с некорректным паролем')
    def test_login_fails_wrong_password(self, existing_user_setup):
        with allure.step('Использовать неверный пароль'):
            user_info = existing_user_setup
            wrong_password = TestConfig.INVALID_DATA

        with allure.step('Отправить запрос с неверным паролем'):
            result = APIClient.login_user(user_info["email"], wrong_password)

        with allure.step('Проверить ошибку аутентификации'):
            assert result.status_code == 401
            assert result.json() == APIResponses.LOGIN_FAILED