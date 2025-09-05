import requests
import ssl
import socket
from datetime import datetime
from urllib.parse import urlparse
from typing import Dict, Any, Optional, Tuple
from config import SSL_WARNING_THRESHOLD, DEFAULT_TIMEOUT

class WebsiteCheker:
    @staticmethod
    def check_availability(url: str, timeout: int = DEFAULT_TIMEOUT) -> Dict[str, Any]:
        """Check for website availability and HTTP status"""
        try:
            start_time = datetime.now()
            response = requests.get(url, timeout=timeout, allow_redirects=True)
            response_time = (datetime.now() - start_time).total_seconds() * 1000

            return {
                'available': True,
                'status_code': response.status_code,
                'response_time_ms': response_time,
                'error': None
            }
        except requests.exceptions.Timeout:
            return {
                'available': False,
                'status_code': None,
                'response_time_ms': None,
                'error': 'Timeout'
            }
        except requests.exceptions.ConnectionError:
            return {
                'available': False,
                'status_code': None,
                'response_time_ms': None,
                'error': 'ConnectionError'
            }
        except requests.exceptions.RequestException as e:
            return {
                'available': False,
                'status_code': None,
                'response_time_ms': None,
                'error': str(e)
            }
        
    @staticmethod
    def check_ssl_certificate(url: str) -> Dict[str, Any]:
        """Check of SSL certificate for website"""
        try:
            parsed_url = urlparse(url)
            hostname = parsed_url.hostname

            if not hostname:
                return {
                    'valid': False,
                    'error': 'Invalid Url',
                    'days_remaining': None
                }
            
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
            
            expire_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
            days_remaining = (expire_date - datetime.now()).days

            return {
                'valid': True,
                'days_remaining': days_remaining,
                'expires_at': expire_date.isoformat(),
                'is_warning': days_remaining < SSL_WARNING_THRESHOLD,
                'error': None
            }
        except ssl.SSLError as e:
            return {'valid': False, 'error': f'SSL Error: {str(e)}', 'days_remaining': None}
        except socket.timeout:
            return {'valid': False, 'error': 'SSL Check Timeout', 'days_remaining': None}
        except Exception as e:
            return {'valid': False, 'error': f'Unexpected error: {str(e)}', 'days_remaining': None}
        
    @staticmethod
    def comprehensive_check(url: str, timeout: int = DEFAULT_TIMEOUT) -> Dict[str, Any]:
        """Complex website checking"""
        result = {
            'url': url, 
            'timestamp': datetime.now().isoformat(),
            'availability': None,
            'ssl': None
        }

        availability = WebsiteCheker.check_availability(url, timeout)
        result['availability'] = availability

        if url.startswith('https://'):
            ssl_check = WebsiteCheker.check_ssl_certificate(url)
            result['ssl'] = ssl_check
        
        return result