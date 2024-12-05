from http import HTTPStatus
from requests import request
from logos_sdk.services import get_headers
from dotenv import load_dotenv
import os


class MerchantServiceException(Exception):
    pass


class MerchantCenterService:
    def __init__(self, url=None):
        load_dotenv()
        self._URL = url or os.environ.get("MERCHANT_CENTER_SERVICE_PATH")
        self._LIST_ACCOUNTS = self._URL + "/account-service/accounts"
        self._LIST_ACCOUNT_STATUSES = self._URL + "/account-service/account-statuses"
        self._LIST_PRODUCTS = self._URL + "/product-service/products"
        self._LIST_PRODUCT_STATUSES = self._URL + "/product-service/product-statuses"
        self._REPORTS_SEARCH = self._URL + "/reports-search"

    def list_accounts(self, merchant_account_id: str, secret_id: str):
        """
        Lists the sub-accounts in your Merchant Center account
        :param merchant_account_id: The ID of the managing account. This must be a multi-client account
        :param secret_id: The ID of the secret in secret manager
        :return: List[Dict]
        """
        body = {"merchant_account_id": merchant_account_id, "secret_id": secret_id}
        header = get_headers(self._LIST_ACCOUNTS)
        response = request("post", url=self._LIST_ACCOUNTS, json=body, headers=header)

        if response.status_code == HTTPStatus.OK:
            service_response = response.json()
            return service_response["data"]
        else:
            raise MerchantServiceException(response.content)

    def list_account_statuses(
            self, merchant_account_id: str, account_id: str, secret_id: str
    ):
        """
        Retrieves the statuses of a Merchant Center account.
        :param merchant_account_id: The ID of the managing account. This must be a multi-client account.
        :param account_id: The ID of the account.
        :param secret_id: The ID of the secret in secret manager
        :return: List[Dict]
        """
        body = {
            "merchant_account_id": merchant_account_id,
            "account_id": account_id,
            "secret_id": secret_id,
        }
        header = get_headers(self._LIST_ACCOUNT_STATUSES)
        response = request(
            "post", url=self._LIST_ACCOUNT_STATUSES, json=body, headers=header
        )

        if response.status_code == HTTPStatus.OK:
            service_response = response.json()
            return service_response["data"]
        else:
            raise MerchantServiceException(response.content)

    def list_products(self, merchant_account_id: str, secret_id: str, page_size: int = 250):
        """
        Lists the products in your Merchant Center account
        :param merchant_account_id: The ID of the managing account. This account cannot be a multi-client account
        :param secret_id: The ID of the secret in secret manager
        :param page_size: size of the page
        :return: List[Dict]
        """
        body = {"merchant_account_id": merchant_account_id, "secret_id": secret_id, "page_size": page_size}
        header = get_headers(self._LIST_PRODUCTS)
        response = request("post", url=self._LIST_PRODUCTS, json=body, headers=header)

        if response.status_code != HTTPStatus.OK:
            raise MerchantServiceException(response.content)

        service_response = response.json()
        yield service_response["data"]["results"]

        while service_response["data"]["nextPageToken"] is not None:
            body["page_token"] = service_response["data"]["nextPageToken"]
            response = request(
                "post", url=self._LIST_PRODUCTS, json=body, headers=header
            )

            if response.status_code != HTTPStatus.OK:
                raise MerchantServiceException(response.content)

            service_response = response.json()
            yield service_response["data"]["results"]

    def list_products_statuses(self, merchant_account_id: str, secret_id: str):
        """
        Lists the statuses of the products in your Merchant Center account
        :param merchant_account_id: The ID of the
        account that contains the products. This account cannot be a multi-client account
        :param secret_id: The ID of the secret in secret manager
        :return: List[Dict]
        """
        body = {"merchant_account_id": merchant_account_id, "secret_id": secret_id}
        header = get_headers(self._LIST_PRODUCT_STATUSES)
        response = request(
            "post", url=self._LIST_PRODUCT_STATUSES, json=body, headers=header
        )

        if response.status_code == HTTPStatus.OK:
            service_response = response.json()
            return service_response["data"]
        else:
            raise MerchantServiceException(response.content)

    def reports_search(
            self,
            merchant_account_id: str,
            secret_id: str,
            query: str,
            page_token: str = None,
            page_size: int = 1000,
    ):
        body = {
            "merchant_account_id": merchant_account_id,
            "secret_id": secret_id,
            "query": query,
            "page_token": page_token,
            "page_size": page_size,
        }
        header = get_headers(self._REPORTS_SEARCH)
        response = request("post", url=self._REPORTS_SEARCH, json=body, headers=header)

        if response.status_code == HTTPStatus.OK:
            service_response = response.json()
            return service_response["data"]
        else:
            raise MerchantServiceException(response.content)

    def reports_search_generator(
            self,
            merchant_account_id: str,
            secret_id: str,
            query: str,
            page_size: int = 1000,
    ):
        body = {
            "merchant_account_id": merchant_account_id,
            "secret_id": secret_id,
            "query": query,
            "page_size": page_size,
        }
        header = get_headers(self._REPORTS_SEARCH)
        response = request("post", url=self._REPORTS_SEARCH, json=body, headers=header)

        if response.status_code != HTTPStatus.OK:
            raise MerchantServiceException(response.content)

        service_response = response.json()
        yield service_response["data"]["results"]

        while service_response["data"]["nextPageToken"] is not None:
            body["page_token"] = service_response["data"]["nextPageToken"]
            response = request(
                "post", url=self._REPORTS_SEARCH, json=body, headers=header
            )

            if response.status_code != HTTPStatus.OK:
                raise MerchantServiceException(response.content)

            service_response = response.json()
            yield service_response["data"]["results"]
