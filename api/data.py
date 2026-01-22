import random
import string
import time

class ServiceURLs:
    API_BASE = 'https://stellarburgers.education-services.ru'
    
    # Пользователь: регистрация и аутентификация
    USER_REGISTRATION = f'{API_BASE}/api/auth/register'
    USER_LOGIN = f'{API_BASE}/api/auth/login'
    USER_PROFILE = f'{API_BASE}/api/auth/user'
    
    # Товары и заказы
    ITEMS_LIST = f'{API_BASE}/api/ingredients'
    ORDER_ENDPOINT = f'{API_BASE}/api/orders'


class APIResponses:
    # пользователь уже существует
    USER_ALREADY_EXISTS = {
        "success": False,
        "message": "User already exists"
    }

    # отсутствуют обязательные поля
    MISSING_REQUIRED_FIELDS = {
        "success": False,
        "message": "Email, password and name are required fields"
    }

    # ошибка входа
    LOGIN_FAILED = {
        "success": False,
        "message": "email or password are incorrect"
    }

    # требуется авторизация
    AUTHORIZATION_REQUIRED = {
        "success": False,
        "message": "You should be authorised"
    }

    # отсутствуют товары
    NO_ITEMS_PROVIDED = {
        "success": False,
        "message": "Ingredient ids must be provided"
    }


class TestConfig:
    # тестовые данные
    INVALID_DATA = 'test_data_789_abcdef'
    
    # некорректные идентификаторы
    BAD_ITEM_IDS = ["wrong-item-id-789-abcdef"]


def create_user_data():
    """Создание тестовых данных пользователя"""
    timestamp = int(time.time())
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    
    name = f"TestUser{timestamp}"
    password = f"Pass{timestamp}{random_part}!"
    email = f"user{timestamp}@testmail.com"
    
    return {
        "email": email,
        "password": password,
        "name": name
    }


def create_product_info():
    """Создание данных товара"""
    return {
        "title": f"Item_{random.randint(1000, 9999)}",
        "price": round(random.uniform(10.0, 1000.0), 2),
        "category": random.choice(["electronics", "clothing", "books"])
    }