import pytest
import allure
from api.api_client import APIClient
from api.data import create_user_data, APIResponses


@allure.feature('Регистрация пользователя')
class TestUserRegistration:
    @allure.title('Успешная регистрация нового пользователя')
    def test_register_new_user_success(self, test_data_cleanup):
        with allure.step('Создать тестовый профиль пользователя'):
            user_profile = create_user_data()
            test_data_cleanup.update(user_profile)

        with allure.step('Выполнить запрос на регистрацию'):
            result = APIClient.register_user(user_profile)

        with allure.step('Проверить успешность регистрации'):
            assert result.status_code == 200
            assert result.json()["success"] == True
            assert result.json()["user"]["email"] == user_profile["email"]

    @allure.title('Невозможность регистрации существующего пользователя')
    def test_register_existing_user_fails(self, existing_user_setup):
        with allure.step('Получить данные активного пользователя'):
            user_info = existing_user_setup

        with allure.step('Повторно отправить запрос регистрации'):
            result = APIClient.register_user(user_info)

        with allure.step('Проверить сообщение о конфликте'):
            assert result.status_code == 403
            assert result.json() == APIResponses.USER_ALREADY_EXISTS

    @pytest.mark.parametrize('required_field', ['email', 'password', 'name'])
    @allure.title('Проверка обязательных полей при регистрации: {required_field}')
    def test_registration_needs_all_fields(self, required_field):
        with allure.step('Создать профиль и удалить обязательное поле'):
            user_profile = create_user_data()
            user_profile.pop(required_field)

        with allure.step('Отправить запрос с отсутствующим полем'):
            result = APIClient.register_user(user_profile)

        with allure.step('Проверить ошибку валидации'):
            assert result.status_code == 403
            assert result.json() == APIResponses.MISSING_REQUIRED_FIELDS