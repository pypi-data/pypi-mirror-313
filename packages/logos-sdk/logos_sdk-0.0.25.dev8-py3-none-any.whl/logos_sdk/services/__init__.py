import google.auth.transport.requests
import google.oauth2.id_token
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def get_headers(route):
    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, route)
    return {
        "Authorization": f"Bearer {id_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def execute_request(method, url, json):
    retry_strategy = Retry(
        total=3,
        raise_on_status=False,
        status_forcelist=[429, 500, 502, 503, 504],
        backoff_factor=1,
        allowed_methods=None
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)
    header = get_headers(url)
    # 70 is magic number, we tolerate the API to tell us to wait 60 seconds max,
    # otherwise we kill it
    response = http.request(method, url=url, json=json, timeout=70, headers=header)

    return response
