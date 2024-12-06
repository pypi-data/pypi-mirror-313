import json
import os
import requests
from typing import Optional, Dict, Any, Union
from urllib.parse import urljoin
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class ClientError(Exception):
    """Base exception for client errors"""
    pass

class AuthenticationError(ClientError):
    """Raised when authentication fails"""
    pass

class ApiError(ClientError):
    """Raised when API returns an error"""
    pass

class BaseClient:
    """Base client for API interactions"""

    def __init__(self, base_url: Optional[str] = None, api_version: Optional[str] = None, config_path: Optional[str] = None):
        """Initialize client with configuration

        Args:
            base_url (Optional[str]): Base URL for API. Defaults to config value.
            api_version (Optional[str]): API version. Defaults to config value.
            config_path (Optional[str]): Path to config file. Defaults to 'config.json' in same directory.
        """
        self.config = self._load_config(config_path)
        self.base_url = base_url or self.config['api']['base_url']
        self.api_version = api_version or self.config['api']['version']
        self.api_key: Optional[str] = None
        self.session = self._configure_session()

    def update_config(self, updates: Dict[str, Any]) -> None:
        """Update configuration with new values

        Args:
            updates (Dict[str, Any]): Configuration updates
        """
        self.config = self._deep_update(self.config, updates)
        # Reconfigure session with new settings
        self.session = self._configure_session()

    def _deep_update(self, base: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
        """Deep update dictionary

        Args:
            base (Dict[str, Any]): Base dictionary
            updates (Dict[str, Any]): Updates to apply

        Returns:
            Dict[str, Any]: Updated dictionary
        """
        for key, value in updates.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                base[key] = self._deep_update(base[key], value)
            else:
                base[key] = value
        return base

    def get_config(self, path: str, default: Any = None) -> Any:
        """Get configuration value by dot notation path

        Args:
            path (str): Configuration path (e.g., 'api.timeout')
            default (Any, optional): Default value if path not found

        Returns:
            Any: Configuration value
        """
        keys = path.split('.')
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

    def save_config(self, config_path: Optional[str] = None) -> None:
        """Save current configuration to file

        Args:
            config_path (Optional[str]): Path to save config file
        """
        if not config_path:
            config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        
        with open(config_path, 'w') as f:
            json.dump(self.config, f, indent=4)

    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration from file

        Args:
            config_path (Optional[str]): Path to config file

        Returns:
            Dict[str, Any]: Configuration dictionary
        """
        if not config_path:
            config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                'api': {
                    'base_url': 'http://localhost:8000',
                    'version': 'v1',
                    'timeout': 30,
                    'retry_attempts': 3,
                    'retry_delay': 1
                },
                'security': {
                    'verify_ssl': True,
                    'api_key_header': 'X-API-Key'
                }
            }

    def _configure_session(self) -> requests.Session:
        """Configure requests session with retry logic and timeouts

        Returns:
            requests.Session: Configured session
        """
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=self.config['api']['retry_attempts'],
            backoff_factor=self.config['api']['retry_delay'],
            status_forcelist=[429, 500, 502, 503, 504]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        # Configure SSL verification
        session.verify = self.config['security']['verify_ssl']
        
        return session
        """Initialize client with base URL

        Args:
            base_url (str): Base URL for API (e.g., 'http://localhost:8000')
            api_version (str, optional): API version. Defaults to 'v1'.
        """
        self.base_url = base_url.rstrip('/')
        self.api_version = api_version
        self.api_key: Optional[str] = None
        self.session = requests.Session()

    def set_api_key(self, api_key: str) -> None:
        """Set the API key for authentication

        Args:
            api_key (str): API key for authentication
        """
        self.api_key = api_key
        header_name = self.config['security']['api_key_header']
        self.session.headers.update({header_name: api_key})

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to API with SSE support

        Args:
            method (str): HTTP method ('GET', 'POST', etc.)
            endpoint (str): API endpoint
            data (Optional[Dict[str, Any]], optional): Request data
            params (Optional[Dict[str, Any]], optional): Query parameters

        Returns:
            Dict[str, Any]: Response data
        """
        """Make HTTP request to API

        Args:
            method (str): HTTP method ('GET', 'POST', etc.)
            endpoint (str): API endpoint (e.g., '/chatbot/create')
            data (Optional[Dict[str, Any]], optional): Request data. Defaults to None.
            params (Optional[Dict[str, Any]], optional): Query parameters. Defaults to None.

        Raises:
            AuthenticationError: When API key is not set
            ApiError: When API returns an error

        Returns:
            Dict[str, Any]: API response data
        """
        if not self.api_key:
            raise AuthenticationError('API key not set. Call set_api_key() first.')

        # Construct URL with API version prefix
        versioned_endpoint = f'/api/{self.api_version}/{endpoint.lstrip("/")}'
        url = urljoin(self.base_url, versioned_endpoint)

        try:
            headers = self.session.headers.copy()
            if 'content-type' not in headers:
                headers['content-type'] = 'application/json'

            # Use configuration values for request
            timeout = timeout or self.config['api']['timeout']
            
            # Add default headers from config
            try:
                user_agent = f'Agents-Client/{self.config["api"]["version"]}'
            except KeyError:
                raise ApiError('Invalid configuration: missing API version')
            headers.update({
                'Accept': 'application/json',
                'User-Agent': user_agent
            })
            
            # Make request with configured settings
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=headers,
                stream=False,
                timeout=timeout
            )
            
            # Log request if enabled in config
            if self.config.get('logging', {}).get('enabled', False):
                print(f'Request to {url} completed with status {response.status_code}')
                if self.config.get('logging', {}).get('level', '').upper() == 'DEBUG':
                    print(f"Request URL: {url}")
                    print(f"Request method: {method}")
                    print(f"Request headers: {headers}")
                    print(f"Response headers: {dict(response.headers)}")

            response.raise_for_status()
            
            # Check for empty response
            if not response.content:
                raise ApiError('Empty response received from server')
            
            # Parse JSON response
            try:
                return response.json()
            except json.JSONDecodeError as e:
                raise ApiError(f'Failed to parse JSON response: {str(e)}\nResponse text: {response.text}')

        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise AuthenticationError('Invalid API key')
            try:
                error_data = response.json()
                error_message = error_data.get('detail', str(e))
            except ValueError:
                error_message = str(e)
            raise ApiError(f'API request failed: {error_message}')

        except requests.exceptions.RequestException as e:
            raise ApiError(f'Request failed: {str(e)}')

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make GET request

        Args:
            endpoint (str): API endpoint
            params (Optional[Dict[str, Any]], optional): Query parameters. Defaults to None.

        Returns:
            Dict[str, Any]: API response data
        """
        return self._make_request('GET', endpoint, params=params)

    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make POST request

        Args:
            endpoint (str): API endpoint
            data (Dict[str, Any]): Request data

        Returns:
            Dict[str, Any]: API response data
        """
        return self._make_request('POST', endpoint, data=data)

    def validate_config(self) -> bool:
        """Validate current configuration

        Returns:
            bool: True if configuration is valid
        """
        required_fields = {
            'api': ['base_url', 'version', 'timeout', 'retry_attempts', 'retry_delay'],
            'security': ['verify_ssl', 'api_key_header'],
            'endpoints': ['auth', 'chatbot', 'agent', 'health'],
            'logging': ['enabled', 'level']
        }

        for section, fields in required_fields.items():
            if section not in self.config:
                print(f'Missing required section: {section}')
                return False
            for field in fields:
                if field not in self.config[section]:
                    print(f'Missing required field: {section}.{field}')
                    return False
        return True

    def process_image(self, image: str) -> Dict[str, str]:
        """Process image input and return formatted image data

        Args:
            image (str): Can be a URL, base64 string, or file path

        Returns:
            Dict[str, str]: Formatted image data with 'type' and 'data' keys
        """
        # Check if it's a URL
        if image.startswith(('http://', 'https://', 'ftp://')):
            return {'type': 'url', 'data': image}

        # Check if it's a base64 string
        try:
            # Try to decode to check if it's valid base64
            import base64
            base64.b64decode(image)
            return {'type': 'base64', 'data': image}
        except:
            pass

        # Assume it's a file path
        try:
            with open(image, 'rb') as f:
                import base64
                image_data = base64.b64encode(f.read()).decode('utf-8')
                return {'type': 'base64', 'data': image_data}
        except Exception as e:
            raise ValueError(f'Invalid image input. Must be a URL, base64 string, or valid file path. Error: {str(e)}')

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make DELETE request

        Args:
            endpoint (str): API endpoint

        Returns:
            Dict[str, Any]: API response data
        """
        return self._make_request('DELETE', endpoint)
