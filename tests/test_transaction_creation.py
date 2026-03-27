import pytest
import allure
from api.api_client import APIClient
from api.data import APIResponses, TestConfig


@allure.feature('Создание заказа')
class TestOrderCreation:

    @allure.title('Создание заказа с авторизацией и корректными товарами')
    def test_place_order_with_auth_success(self, existing_user_setup, get_available_items):
        user_info = existing_user_setup

        with allure.step('Получить токен авторизации'):
            from conftest import get_user_token
            user_token = get_user_token(user_info)

        with allure.step('Создать заказ с товарами'):
            result = APIClient.place_order(get_available_items, user_token)

        with allure.step('Проверить успешность создания'):
            assert result.status_code == 200
            assert result.json()["success"] == True

    @allure.title('Создание заказа без товаров')
    def test_place_order_empty_items_fails(self, existing_user_setup):
        user_info = existing_user_setup

        with allure.step('Получить токен авторизации'):
            from conftest import get_user_token
            user_token = get_user_token(user_info)

        with allure.step('Отправить запрос с пустым списком товаров'):
            result = APIClient.place_order([], user_token)

        with allure.step('Проверить ошибку валидации'):
            assert result.status_code == 400
            assert result.json() == APIResponses.NO_ITEMS_PROVIDED

    @allure.title('Создание заказа с некорректными идентификаторами товаров')
    def test_place_order_invalid_item_ids(self, existing_user_setup):
        user_info = existing_user_setup

        with allure.step('Получить токен авторизации'):
            from conftest import get_user_token
            user_token = get_user_token(user_info)

        with allure.step('Использовать некорректные идентификаторы'):
            result = APIClient.place_order(TestConfig.BAD_ITEM_IDS, user_token)

        with allure.step('Проверить ответ сервера'):
            assert result.status_code in [400, 500]

    @allure.title('Создание заказа без авторизации')
    def test_place_order_without_auth_success(self, get_available_items):
        with allure.step('Отправить запрос без токена'):
            result = APIClient.place_order(get_available_items)

        with allure.step('Проверить успешное создание заказа'):
            assert result.status_code == 200
            assert result.json()["success"] == True