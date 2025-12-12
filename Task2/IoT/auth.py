"""
Модуль авторизації для IoT пристрою MyDogSpace
Забезпечує реєстрацію та вхід користувачів через API
"""

import urequests
import ujson
import config


class AuthManager:
    """Клас для управління авторизацією"""

    def __init__(self):
        self.token = None
        self.user_id = None
        self.username = None

    def register(self, username, email, password, admin_code=None):
        """
        Реєстрація нового користувача

        Args:
            username: Ім'я користувача
            email: Email адреса
            password: Пароль
            admin_code: Опціональний код адміністратора

        Returns:
            bool: True якщо реєстрація успішна, False інакше
        """
        url = config.API_BASE_URL + config.API_AUTH_REGISTER

        payload = {
            "username": username,
            "email": email,
            "password": password
        }

        if admin_code:
            payload["adminCode"] = admin_code

        try:
            if config.DEBUG:
                print(f"[AUTH] Реєстрація користувача: {username}")
                print(f"[AUTH] URL: {url}")

            response = urequests.post(
                url,
                headers={"Content-Type": "application/json"},
                data=ujson.dumps(payload)
            )

            if config.DEBUG:
                print(f"[AUTH] Статус відповіді: {response.status_code}")

            if response.status_code == 200:
                print(f"[AUTH] ✓ Користувач {username} успішно зареєстрований")
                response.close()
                return True
            else:
                error_data = response.json()
                print(f"[AUTH] ✗ Помилка реєстрації: {error_data.get('message', 'Невідома помилка')}")
                response.close()
                return False

        except Exception as e:
            print(f"[AUTH] ✗ Виняток при реєстрації: {e}")
            return False

    def login(self, email, password):
        """
        Вхід користувача та отримання JWT токену

        Args:
            email: Email адреса
            password: Пароль

        Returns:
            bool: True якщо вхід успішний, False інакше
        """
        url = config.API_BASE_URL + config.API_AUTH_LOGIN

        payload = {
            "email": email,
            "password": password
        }

        try:
            if config.DEBUG:
                print(f"[AUTH] Вхід користувача: {email}")
                print(f"[AUTH] URL: {url}")

            response = urequests.post(
                url,
                headers={"Content-Type": "application/json"},
                data=ujson.dumps(payload)
            )

            if config.DEBUG:
                print(f"[AUTH] Статус відповіді: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                self.token = data.get("token")

                # Декодування токену для отримання user_id (базова реалізація)
                # У реальному JWT токен містить інформацію в base64
                if self.token:
                    print(f"[AUTH] ✓ Успішний вхід. Токен отримано")
                    if config.DEBUG:
                        print(f"[AUTH] Token: {self.token[:50]}...")
                    response.close()
                    return True
                else:
                    print("[AUTH] ✗ Токен не отримано")
                    response.close()
                    return False
            else:
                error_data = response.json()
                print(f"[AUTH] ✗ Помилка входу: {error_data.get('message', 'Невірні дані')}")
                response.close()
                return False

        except Exception as e:
            print(f"[AUTH] ✗ Виняток при вході: {e}")
            return False

    def get_auth_header(self):
        """
        Повертає заголовок авторизації для API запитів

        Returns:
            dict: Словник з заголовком Authorization
        """
        if not self.token:
            return {}

        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def is_authenticated(self):
        """
        Перевіряє чи користувач авторизований

        Returns:
            bool: True якщо є токен, False інакше
        """
        return self.token is not None

    def logout(self):
        """Вихід користувача (очищення токену)"""
        self.token = None
        self.user_id = None
        self.username = None
        print("[AUTH] Вихід виконано")


# Глобальний екземпляр менеджера авторизації
auth_manager = AuthManager()
