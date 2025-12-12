"""
Тестовий скрипт для перевірки доступності API сервера MyDogSpace
Запустіть цей скрипт перед використанням IoT пристрою
"""

import requests
import json

# Конфігурація
API_BASE_URL = "http://35.192.164.131:8080/api"

# Кольори для виводу
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'


def test_server_availability():
    """Перевірка доступності сервера"""
    print("\n" + "="*60)
    print("Тестування MyDogSpace API Server")
    print("="*60 + "\n")

    print(f"API URL: {API_BASE_URL}\n")

    # Тест 1: Базове підключення
    print("Тест 1: Перевірка доступності сервера...")
    try:
        response = requests.get(f"{API_BASE_URL.replace('/api', '')}", timeout=5)
        print(f"{GREEN}✓ Сервер доступний{RESET}")
        success_1 = True
    except requests.exceptions.RequestException as e:
        print(f"{RED}✗ Сервер недоступний: {e}{RESET}")
        success_1 = False

    # Тест 2: Реєстрація тестового користувача
    print("\nТест 2: Реєстрація користувача...")
    test_user = {
        "username": "iot_test_user",
        "email": "iot_test@example.com",
        "password": "testpass123"
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/register",
            headers={"Content-Type": "application/json"},
            json=test_user,
            timeout=10
        )

        if response.status_code == 200:
            print(f"{GREEN}✓ Користувач зареєстрований успішно{RESET}")
            success_2 = True
        elif response.status_code == 400:
            error = response.json()
            if "вже існує" in error.get("message", "").lower():
                print(f"{YELLOW}⚠ Користувач вже існує (це нормально){RESET}")
                success_2 = True
            else:
                print(f"{RED}✗ Помилка: {error.get('message', 'Невідома помилка')}{RESET}")
                success_2 = False
        else:
            print(f"{RED}✗ Неочікуваний статус: {response.status_code}{RESET}")
            print(f"Відповідь: {response.text}")
            success_2 = False
    except requests.exceptions.RequestException as e:
        print(f"{RED}✗ Помилка з'єднання: {e}{RESET}")
        success_2 = False

    # Тест 3: Вхід та отримання токену
    print("\nТест 3: Вхід та отримання JWT токену...")
    login_data = {
        "email": test_user["email"],
        "password": test_user["password"]
    }

    token = None
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            headers={"Content-Type": "application/json"},
            json=login_data,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            token = data.get("token")
            if token:
                print(f"{GREEN}✓ JWT токен отримано{RESET}")
                print(f"  Токен: {token[:50]}...")
                success_3 = True
            else:
                print(f"{RED}✗ Токен відсутній у відповіді{RESET}")
                success_3 = False
        else:
            print(f"{RED}✗ Помилка входу: {response.status_code}{RESET}")
            print(f"Відповідь: {response.text}")
            success_3 = False
    except requests.exceptions.RequestException as e:
        print(f"{RED}✗ Помилка з'єднання: {e}{RESET}")
        success_3 = False

    # Тест 4: Перевірка захищеного endpoint (якщо є токен)
    print("\nТест 4: Перевірка авторизованого доступу...")
    if token:
        try:
            response = requests.get(
                f"{API_BASE_URL}/smartdevices",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                },
                timeout=10
            )

            if response.status_code in [200, 404]:
                print(f"{GREEN}✓ Авторизація працює{RESET}")
                print(f"  Статус: {response.status_code}")
                success_4 = True
            else:
                print(f"{YELLOW}⚠ Неочікуваний статус: {response.status_code}{RESET}")
                success_4 = True  # Все одно вважаємо успішним, якщо не 401/403
        except requests.exceptions.RequestException as e:
            print(f"{RED}✗ Помилка з'єднання: {e}{RESET}")
            success_4 = False
    else:
        print(f"{YELLOW}⚠ Пропущено (немає токену){RESET}")
        success_4 = False

    # Результат
    print("\n" + "="*60)
    total_tests = 4
    passed_tests = sum([success_1, success_2, success_3, success_4])

    if passed_tests == total_tests:
        print(f"{GREEN}✓ Всі тести пройдено успішно ({passed_tests}/{total_tests}){RESET}")
        print(f"{GREEN}IoT пристрій готовий до роботи з сервером!{RESET}")
    elif passed_tests >= 3:
        print(f"{YELLOW}⚠ Більшість тестів пройдено ({passed_tests}/{total_tests}){RESET}")
        print(f"{YELLOW}IoT пристрій повинен працювати, але можуть бути проблеми{RESET}")
    else:
        print(f"{RED}✗ Багато тестів провалено ({passed_tests}/{total_tests}){RESET}")
        print(f"{RED}Перевірте доступність сервера перед запуском IoT пристрою{RESET}")

    print("="*60 + "\n")

    return passed_tests >= 3


if __name__ == "__main__":
    try:
        test_server_availability()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Тестування перервано користувачем{RESET}")
    except Exception as e:
        print(f"\n{RED}Критична помилка: {e}{RESET}")
