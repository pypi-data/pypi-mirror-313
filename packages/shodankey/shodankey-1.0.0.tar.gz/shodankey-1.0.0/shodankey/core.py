import requests
import re
from datetime import datetime
from typing import Dict, Any

class ShodanAPIKeyValidator:
    def __init__(self, api_key: str) -> None:
        self.api_key: str = api_key
        self.base_url: str = 'https://api.shodan.io/api-info'

    def validate_key_format(self) -> bool:
        key_pattern: str = r'^[a-zA-Z0-9]{32}$'
        if not re.match(key_pattern, self.api_key):
            print("Warning: Invalid API key format.")
            return False
        return True

    def check_api_key_validity(self) -> Dict[str, Any]:
        if not self.validate_key_format():
            return {"valid": False, "error": "Invalid API key format"}

        try:
            response: requests.Response = requests.get(
                self.base_url, params={'key': self.api_key}, timeout=10
            )
            if response.status_code == 200:
                return self._process_successful_response(response)
            if response.status_code == 401:
                return {"valid": False, "error": "Unauthorized - Invalid API Key"}
            return {"valid": False, "error": f"Unexpected response: {response.status_code}"}
        except requests.RequestException as e:
            return {"valid": False, "error": f"Network error: {str(e)}"}

    def _process_successful_response(self, response: requests.Response) -> Dict[str, Any]:
        data: Dict[str, Any] = response.json()
        return {
            "valid": True,
            "plan": data.get('plan', 'Unknown'),
            "credits": data.get('credits', 0),
            "usage_limits": {
                "scan_credits": data.get('usage_limits', {}).get('scan_credits', 0),
                "query_credits": data.get('usage_limits', {}).get('query_credits', 0),
                "monitored_ips": data.get('usage_limits', {}).get('monitored_ips', 0)
            },
            "scan_credits": data.get('scan_credits', 0),
            "query_credits": data.get('query_credits', 0),
            "monitored_ips": data.get('monitored_ips', 0),
            "unlocked_left": data.get('unlocked_left', 0),
            "telnet": data.get('telnet', False),
            "https": data.get('https', False),
            "timestamp": datetime.now().isoformat()
        }

def token(api_key: str) -> Dict[str, Any]:
    validator: ShodanAPIKeyValidator = ShodanAPIKeyValidator(api_key)
    return validator.check_api_key_validity()
