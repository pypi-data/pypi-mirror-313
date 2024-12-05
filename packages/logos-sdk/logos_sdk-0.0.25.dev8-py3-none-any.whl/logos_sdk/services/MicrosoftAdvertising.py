from http import HTTPStatus
from requests import request
from logos_sdk.services import get_headers
from typing import List
from dotenv import load_dotenv
import os


class MicrosoftAdvertisingException(Exception):
    pass


# https://learn.microsoft.com/en-us/advertising/reporting-service/adgroupstatusreportfilter?view=bingads-13
class EntityStatus:
    ACTIVE = "Active"
    DELETED = "Deleted"
    EXPIRED = "Expired"
    PAUSED = "Paused"


class MicrosoftAdvertising:
    def __init__(self, url=None):
        load_dotenv()
        self._URL = url or os.environ.get("MICROSOFT_ADVERTISING_PATH")
        self._GET_ACCESSIBLE_ACCOUNTS = self._URL + "/accessible-accounts"
        self._GET_DESTINATION_URL_REPORT = self._URL + "/destination-url-report"
        self._GET_CAMPAIGN_PERFORMANCE_REPORT = self._URL + "/campaign-performance-report"
        self._GET_GEOGRAPHIC_PERFORMANCE_REPORT = self._URL + "/geographic-performance-report"
        self._GET_BUDGET_SUMMARY_REPORT = self._URL + "/budget-summary-report"

    def get_destination_url_report(
        self,
        account_id: str,
        secret_id: str,
        date_from: str,
        date_to: str,
        report_columns: List[str],
        entity_statuses: dict = None,
    ) -> List:
        """
        Calls endpoint for getting destination URL stats
        https://learn.microsoft.com/en-us/advertising/reporting-service/destinationurlperformancereportrequest?view=bingads-13
        :param account_id: The ID of the account in Microsoft Advertising
        :param secret_id: The ID of the secret in secret manager
        :param date_from: The date we want the report to start from. Must be before date to
        :param date_to: The date we want the report to end at
        :param report_columns: stats we want included in the report
        :param entity_statuses: dict containing status ad_status, ad_group_status, campaign_status and account_status
        :return: List of urls and their stats
        """
        if entity_statuses is None:
            entity_statuses = {
                "ad_status": EntityStatus.ACTIVE,
                "ad_group_status": EntityStatus.ACTIVE,
                "campaign_status": EntityStatus.ACTIVE,
                "account_status": EntityStatus.ACTIVE,
            }

        body = {
            "account_id": account_id,
            "secret_id": secret_id,
            "date_from": date_from,
            "date_to": date_to,
            "report_columns": report_columns,
        } | entity_statuses

        header = get_headers(self._GET_DESTINATION_URL_REPORT)
        response = request(
            "post", url=self._GET_DESTINATION_URL_REPORT, json=body, headers=header
        )

        if response.status_code == HTTPStatus.OK:
            service_response = response.json()
            return service_response["data"]
        else:
            raise MicrosoftAdvertisingException(response.content)

    def get_geographic_report(
        self,
        account_id: str,
        secret_id: str,
        date_from: str,
        date_to: str,
        report_columns: List[str],
        entity_statuses: dict = None,
    ) -> List:
        """
        Calls endpoint for getting geographic stats
        https://learn.microsoft.com/en-us/advertising/reporting-service/geographicperformancereportrequest?view=bingads-13&tabs=xml
        :param account_id: The ID of the account in Microsoft Advertising
        :param secret_id: The ID of the secret in secret manager
        :param date_from: The date we want the report to start from. Must be before date to
        :param date_to: The date we want the report to end at
        :param report_columns: stats we want included in the report
        :param entity_statuses: dict containing status ad_group_status, campaign_status and account_status
        :return: List of campaigns and their geographic stats
        """
        if entity_statuses is None:
            entity_statuses = {
                "ad_group_status": EntityStatus.ACTIVE,
                "campaign_status": EntityStatus.ACTIVE,
                "account_status": EntityStatus.ACTIVE,
            }

        body = {
            "account_id": account_id,
            "secret_id": secret_id,
            "date_from": date_from,
            "date_to": date_to,
            "report_columns": report_columns,
        } | entity_statuses

        header = get_headers(self._GET_GEOGRAPHIC_PERFORMANCE_REPORT)
        response = request(
            "post", url=self._GET_GEOGRAPHIC_PERFORMANCE_REPORT, json=body, headers=header
        )

        if response.status_code == HTTPStatus.OK:
            service_response = response.json()
            return service_response["data"]
        else:
            raise MicrosoftAdvertisingException(response.content)

    def get_campaign_performance_report(
        self,
        account_id: str,
        secret_id: str,
        date_from: str,
        date_to: str,
        report_columns: List[str],
        entity_statuses: dict = None,
    ) -> List:
        """
        Calls endpoint for getting campaign performance stats
        https://learn.microsoft.com/en-us/advertising/reporting-service/campaignperformancereportrequest?view=bingads-13
        :param account_id: The ID of the account in Microsoft Advertising
        :param secret_id: The ID of the secret in secret manager
        :param date_from: The date we want the report to start from. Must be before date to
        :param date_to: The date we want the report to end at
        :param report_columns: stats we want included in the report
        :param entity_statuses: dict containing status of status and account_status
        :return: List of campaigns and their stats
        """
        if entity_statuses is None:
            entity_statuses = {
                "status": EntityStatus.ACTIVE,
                "account_status": EntityStatus.ACTIVE,
            }

        body = {
            "account_id": account_id,
            "secret_id": secret_id,
            "date_from": date_from,
            "date_to": date_to,
            "report_columns": report_columns,
        } | entity_statuses

        header = get_headers(self._GET_CAMPAIGN_PERFORMANCE_REPORT)
        response = request(
            "post", url=self._GET_CAMPAIGN_PERFORMANCE_REPORT, json=body, headers=header
        )

        if response.status_code == HTTPStatus.OK:
            service_response = response.json()
            return service_response["data"]
        else:
            raise MicrosoftAdvertisingException(response.content)

    def get_budget_summary_report(
        self,
        account_id: str,
        secret_id: str,
        date_from: str,
        date_to: str,
        report_columns: List[str]
    ):
        """
        Calls endpoint for getting budget summary
        https://learn.microsoft.com/en-us/advertising/reporting-service/budgetsummaryreportcolumn?view=bingads-13
        :param account_id: The ID of the account in Microsoft Advertising
        :param secret_id: The ID of the secret in secret manager
        :param date_from: The date we want the report to start from. Must be before date to
        :param date_to: The date we want the report to end at
        :param report_columns: stats we want included in the report
        :return: List of campaigns and their stats
        """

        body = {
            "account_id": account_id,
            "secret_id": secret_id,
            "date_from": date_from,
            "date_to": date_to,
            "report_columns": report_columns,
        }

        header = get_headers(self._GET_BUDGET_SUMMARY_REPORT)
        response = request(
            "post", url=self._GET_BUDGET_SUMMARY_REPORT, json=body, headers=header
        )

        if response.status_code == HTTPStatus.OK:
            service_response = response.json()
            return service_response["data"]
        else:
            raise MicrosoftAdvertisingException(response.content)

    def get_accessible_accounts(self, secret_id: str) -> List[dict]:
        """
        Gets
        :param secret_id: The ID of the secret in secret manager
        :return: List of dicts with account_id and name keys
        """
        body = {
            "secret_id": secret_id,
        }
        header = get_headers(self._GET_ACCESSIBLE_ACCOUNTS)
        response = request(
            "post", url=self._GET_ACCESSIBLE_ACCOUNTS, json=body, headers=header
        )

        if response.status_code == HTTPStatus.OK:
            service_response = response.json()
            return service_response["data"]
        else:
            raise MicrosoftAdvertisingException(response.content)
