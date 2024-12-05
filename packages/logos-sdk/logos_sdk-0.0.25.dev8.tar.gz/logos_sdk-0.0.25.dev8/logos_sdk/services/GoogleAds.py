from requests import request
from requests.exceptions import Timeout
from typing import List, Union, Dict
from logos_sdk.services import get_headers
from http import HTTPStatus
from dotenv import load_dotenv
import os
import time
import random


class GoogleAdsServiceException(Exception):
    pass


class GoogleAdsService:
    def __init__(self, url=None):
        load_dotenv()
        self._URL = url or os.environ.get("GOOGLE_ADS_SERVICE_PATH")
        self._SEARCH_STREAM = self._URL + "/search-stream"
        self._SEARCH = self._URL + "/search"
        self._EXCLUDE_FOR_ACCOUNT = self._URL + "/exclude-for-account"
        self._EXCLUDE_FOR_AD_GROUP = self._URL + "/exclude-for-ad-group"

    @staticmethod
    def fetch_with_retry_on_timeout(url, json, headers):
        for attempt in range(5):
            try:
                return request("post", url, json=json, headers=headers, timeout=25)
            except Timeout:
                delay = 2 * (2 ** attempt) + random.randint(0, 9)
                print(f"there was a timeout when contacting the service, going to sleep for {delay} seconds")
                time.sleep(delay)

        raise Exception("The service is not able to reply within 30 seconds.")

    def search_stream(
        self,
        query: str,
        queried_account_id: str,
        secret_id: str,
    ) -> List[Union[List, Dict]]:
        """
        :param query Sql query for google ads. Best way to build it is https://developers.google.com/google-ads/api/fields/v14/accessible_bidding_strategy_query_builder
        :param queried_account_id Google ads id of queried account
        :param secret_id The ID of the secret in secret manager
        :return: List(List)
        """
        body = {
            "query": query,
            "queried_account_id": queried_account_id,
            "secret_id": secret_id,
        }

        header = get_headers(self._SEARCH_STREAM)
        response = self.fetch_with_retry_on_timeout(url=self._SEARCH_STREAM, json=body, headers=header)

        if response.status_code == HTTPStatus.OK:
            service_response = response.json()
            return service_response["data"]
        else:
            raise GoogleAdsServiceException(response.content)

    def search(
        self,
        query: str,
        queried_account_id: str,
        secret_id: str,
        page_size: int,
    ) -> List[Dict]:
        """
        :param query Sql query for google ads. Best way to build it is https://developers.google.com/google-ads/api/fields/v14/accessible_bidding_strategy_query_builder
        :param queried_account_id Google ads id of queried account
        :param secret_id The ID of the secret in secret manager
        :param page_size Size of page for results
        :return {"next_page_token": token, results: list of dict where key for each dict is "metrics" and then metric type from query}
        """
        body = {
            "query": query,
            "queried_account_id": queried_account_id,
            "secret_id": secret_id,
            "page_token": None,
            "page_size": page_size,
        }

        header = get_headers(self._SEARCH)
        response = self.fetch_with_retry_on_timeout(url=self._SEARCH, json=body, headers=header)

        if response.status_code != HTTPStatus.OK:
            raise GoogleAdsServiceException(response.content)

        service_response = response.json()
        yield service_response["data"]["results"]

        # if there was a last page response is empty string
        while service_response["data"]["next_page_token"]:
            body["page_token"] = service_response["data"]["next_page_token"]
            response = request("post", url=self._SEARCH, json=body, headers=header)

            if response.status_code != HTTPStatus.OK:
                raise GoogleAdsServiceException(response.content)

            service_response = response.json()
            yield service_response["data"]["results"]

    def exclude_criterion_for_account(
        self, client_id: str, exclusion_raw: List[str], mode: str, secret_id: str = None
    ) -> None:
        """
        Excludes list of unwanted urls/YouTube channels for account with client_id
        :param client_id: Google Ads id without -
        :param exclusion_raw: list of negative urls/YouTube channels
        :param mode: Union(placement, youtube)
        :param secret_id: id of the secret
        :return: None
        """
        body = {
            "client_id": client_id,
            "exclusion_raw": exclusion_raw,
            "mode": mode,
            "secret_id": secret_id,
        }

        header = get_headers(self._EXCLUDE_FOR_ACCOUNT)
        response = request(
            "post", url=self._EXCLUDE_FOR_ACCOUNT, json=body, headers=header
        )

        if response.status_code == HTTPStatus.OK:
            service_response = response.json()
            return service_response["data"]
        else:
            raise GoogleAdsServiceException(response.content)

    def exclude_criterion_for_ad_group(
        self,
        client_id: str,
        ad_group_id: str,
        exclusion_raw: List[str],
        secret_id: str = None,
    ) -> None:
        """
        Excludes list of unwanted urls/YouTube channels for given ad_group with client_id
        :param client_id: Google Ads id without -
        :param ad_group_id: given ad group id for which urls should be excluded
        :param exclusion_raw: list of negative urls/YouTube channels
        :param secret_id: id of the secret
        :return:None
        """
        body = {
            "client_id": client_id,
            "exclusion_raw": exclusion_raw,
            "ad_group_id": ad_group_id,
            "secret_id": secret_id,
        }

        header = get_headers(self._EXCLUDE_FOR_AD_GROUP)
        response = request(
            "post", url=self._EXCLUDE_FOR_AD_GROUP, json=body, headers=header
        )

        if response.status_code == HTTPStatus.OK:
            return
        else:
            raise GoogleAdsServiceException(response.content)
