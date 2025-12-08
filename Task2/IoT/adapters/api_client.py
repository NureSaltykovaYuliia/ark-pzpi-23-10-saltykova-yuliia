"""
API Client Adapter (Infrastructure Layer)
Адаптер API клієнта (Інфраструктурний шар)
"""
import json


class APIClient:
    """
    HTTP API client for communicating with MyDogSpace backend
    HTTP API клієнт для комунікації з MyDogSpace бекендом
    """

    def __init__(self, base_url: str, timeout=10):
        """
        Initialize API client

        Args:
            base_url: Base URL of the API (e.g., "http://192.168.1.100:5104/api")
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout * 1000  # Convert to milliseconds for urequests
        self.auth_token = None

    def set_auth_token(self, token: str):
        """
        Set JWT authentication token
        Встановити JWT токен аутентифікації
        """
        self.auth_token = token

    def _get_headers(self, include_auth=True):
        """
        Get HTTP headers for requests
        Отримати HTTP заголовки для запитів
        """
        headers = {
            'Content-Type': 'application/json'
        }

        if include_auth and self.auth_token:
            headers['Authorization'] = f'Bearer {self.auth_token}'

        return headers

    def _make_request(self, method: str, endpoint: str, data=None, include_auth=True):
        """
        Make HTTP request to API
        Виконати HTTP запит до API

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (e.g., "/smartdevices")
            data: Request body data (will be JSON encoded)
            include_auth: Whether to include authentication header

        Returns:
            Response data as dict, or None if request failed
        """
        try:
            import urequests
        except ImportError:
            print("[ERROR] urequests module not available")
            return None

        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers(include_auth)

        print(f"[API] {method} {url}")

        try:
            if method == 'GET':
                response = urequests.get(url, headers=headers, timeout=self.timeout)
            elif method == 'POST':
                json_data = json.dumps(data) if data else None
                response = urequests.post(url, headers=headers, data=json_data, timeout=self.timeout)
            elif method == 'PUT':
                json_data = json.dumps(data) if data else None
                response = urequests.put(url, headers=headers, data=json_data, timeout=self.timeout)
            elif method == 'DELETE':
                response = urequests.delete(url, headers=headers, timeout=self.timeout)
            else:
                print(f"[ERROR] Unsupported HTTP method: {method}")
                return None

            print(f"[API] Response status: {response.status_code}")

            # Check if request was successful (2xx status code)
            if 200 <= response.status_code < 300:
                # Parse JSON response if available
                if response.text:
                    try:
                        return response.json()
                    except:
                        return {'status': 'success'}
                return {'status': 'success'}
            else:
                print(f"[ERROR] API request failed: {response.status_code}")
                print(f"[ERROR] Response: {response.text}")
                return None

        except Exception as e:
            print(f"[ERROR] API request exception: {e}")
            return None
        finally:
            if 'response' in locals():
                response.close()

    def register_device(self, device_guid: str, dog_id: int) -> int:
        """
        Register new smart device with API
        Зареєструвати новий розумний пристрій в API

        POST /api/smartdevices
        Body: { "deviceGuid": "...", "dogId": ... }

        Args:
            device_guid: Unique device identifier
            dog_id: ID of the dog to attach device to

        Returns:
            Device ID if successful, None otherwise
        """
        endpoint = "/smartdevices"
        data = {
            "deviceGuid": device_guid,
            "dogId": dog_id
        }

        response = self._make_request('POST', endpoint, data, include_auth=True)

        if response and 'id' in response:
            return response['id']
        return None

    def update_device(self, device_id: int, update_data: dict) -> bool:
        """
        Update smart device data (GPS coordinates and battery level)
        Оновити дані розумного пристрою (GPS координати та рівень батареї)

        PUT /api/smartdevices/{id}
        Body: { "lastLatitude": ..., "lastLongitude": ..., "batteryLevel": ... }

        Args:
            device_id: ID of the device
            update_data: Dictionary with lastLatitude, lastLongitude, batteryLevel

        Returns:
            True if successful, False otherwise
        """
        endpoint = f"/smartdevices/{device_id}"
        response = self._make_request('PUT', endpoint, update_data, include_auth=True)
        return response is not None

    def get_device(self, device_id: int) -> dict:
        """
        Get smart device information by ID
        Отримати інформацію про розумний пристрій за ID

        GET /api/smartdevices/{id}

        Args:
            device_id: ID of the device

        Returns:
            Device data as dict, or None if not found
        """
        endpoint = f"/smartdevices/{device_id}"
        return self._make_request('GET', endpoint, include_auth=True)

    def get_device_by_dog(self, dog_id: int) -> dict:
        """
        Get smart device by dog ID
        Отримати розумний пристрій за ID собаки

        GET /api/smartdevices/dog/{dogId}

        Args:
            dog_id: ID of the dog

        Returns:
            Device data as dict, or None if not found
        """
        endpoint = f"/smartdevices/dog/{dog_id}"
        return self._make_request('GET', endpoint, include_auth=True)

    def delete_device(self, device_id: int) -> bool:
        """
        Delete smart device
        Видалити розумний пристрій

        DELETE /api/smartdevices/{id}

        Args:
            device_id: ID of the device

        Returns:
            True if successful, False otherwise
        """
        endpoint = f"/smartdevices/{device_id}"
        response = self._make_request('DELETE', endpoint, include_auth=True)
        return response is not None

    def login(self, email: str, password: str) -> str:
        """
        Login and get authentication token
        Авторизуватися і отримати токен аутентифікації

        POST /api/auth/login
        Body: { "email": "...", "password": "..." }

        Args:
            email: User email
            password: User password

        Returns:
            JWT token if successful, None otherwise
        """
        endpoint = "/auth/login"
        data = {
            "email": email,
            "password": password
        }

        response = self._make_request('POST', endpoint, data, include_auth=False)

        if response and 'token' in response:
            self.auth_token = response['token']
            return self.auth_token
        return None

    def __repr__(self):
        auth_status = "authenticated" if self.auth_token else "not authenticated"
        return f"APIClient(base_url={self.base_url}, {auth_status})"


class APIClientMock:
    """
    Mock API client for testing without actual backend
    Макет API клієнта для тестування без реального бекенду
    """

    def __init__(self, base_url: str = "http://mock-api.com"):
        self.base_url = base_url
        self.auth_token = "mock-token-12345"
        self.mock_device_id = 1

    def set_auth_token(self, token: str):
        """Set mock auth token"""
        self.auth_token = token

    def register_device(self, device_guid: str, dog_id: int) -> int:
        """Return mock device ID"""
        print(f"[MOCK] Registering device: {device_guid} for dog {dog_id}")
        return self.mock_device_id

    def update_device(self, device_id: int, update_data: dict) -> bool:
        """Simulate successful update"""
        print(f"[MOCK] Updating device {device_id}: {update_data}")
        return True

    def get_device(self, device_id: int) -> dict:
        """Return mock device data"""
        return {
            'id': device_id,
            'deviceGuid': 'MOCK-DEVICE',
            'lastLatitude': 50.4501,
            'lastLongitude': 30.5234,
            'batteryLevel': 85.0,
            'dogId': 1
        }

    def login(self, email: str, password: str) -> str:
        """Return mock token"""
        print(f"[MOCK] Login: {email}")
        return self.auth_token
