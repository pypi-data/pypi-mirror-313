from collections.abc import Iterable
from typing import Any

from sapiopylib.rest.DataMgmtService import DataMgmtServer
from sapiopylib.rest.User import SapioUser
from sapiopylib.rest.pojo.CustomReport import ReportColumn, CustomReport
from sapiopylib.rest.pojo.webhook.WebhookContext import SapioWebhookContext


# FR-46064 - Initial port of PyWebhookUtils to sapiopycommons.
class CustomReportUtil:
    @staticmethod
    def run_system_report(context: SapioWebhookContext | SapioUser,
                          report_name: str,
                          filters: dict[str, Iterable[Any]] | None = None,
                          page_limit: int | None = None) -> list[dict[str, Any]]:
        """
        Run a system report and return the results of that report as a list of dictionaries for the values of each
        column in each row.

        System reports are also known as predefined searches in the system and must be defined in the data designer for
        a specific data type. That is, saved searches created by users cannot be run using this function.

        :param context: The current webhook context or a user object to send requests from.
        :param report_name: The name of the system report to run.
        :param filters: If provided, filter the results of the report using the given mapping of headers to values to
            filter on. Only those headers that both the filters and the custom report share will take effect. That is,
            any filters that have a header name that isn't in the custom report will be ignored.
        :param page_limit: The maximum number of pages to query. If None, exhausts all possible pages.
        :return: The results of the report listed row by row, mapping each cell to the header it is under. The header
            values in the dicts are the data field names of the columns.
        """
        results = CustomReportUtil.__exhaust_system_report(context, report_name, page_limit)
        columns: list[ReportColumn] = results[0]
        rows: list[list[Any]] = results[1]

        ret: list[dict[str, Any]] = []
        for row in rows:
            row_data: dict[str, Any] = {}
            filter_row: bool = False
            for value, column in zip(row, columns):
                header: str = column.data_field_name
                if filters is not None and header in filters and value not in filters.get(header):
                    filter_row = True
                    break
                row_data.update({header: value})
            if filter_row is False:
                ret.append(row_data)
        return ret

    @staticmethod
    def get_system_report_criteria(context: SapioWebhookContext | SapioUser, report_name: str) -> CustomReport:
        """
        Retrieve a custom report from the system given the name of the report. This works by querying the system report
        with a page number and size of 1 to minimize the amount of data transfer needed to retrieve the report's config.

        System reports are also known as predefined searches in the system and must be defined in the data designer for
        a specific data type. That is, saved searches created by users cannot be run using this function.

        Using this, you can add to the root term of the search to then run a new search, or provide it to client
        callbacks or directives that take CustomReports.

        :param context: The current webhook context or a user object to send requests from.
        :param report_name: The name of the system report to run.
        :return: The CustomReport object for the given system report name.
        """
        user: SapioUser = context if isinstance(context, SapioUser) else context.user
        report_man = DataMgmtServer.get_custom_report_manager(user)
        return report_man.run_system_report_by_name(report_name, 1, 1)

    @staticmethod
    def __exhaust_system_report(context: SapioWebhookContext | SapioUser, report_name: str, page_limit: int | None = None) \
            -> tuple[list[ReportColumn], list[list[Any]]]:
        user: SapioUser = context if isinstance(context, SapioUser) else context.user
        report_man = DataMgmtServer.get_custom_report_manager(user)

        report = None
        page_size: int | None = None
        page_number: int | None = None
        has_next_page: bool = True
        rows: list[list[Any]] = []
        cur_page: int = 1
        while has_next_page and (not page_limit or cur_page < page_limit):
            report = report_man.run_system_report_by_name(report_name, page_size, page_number)
            page_size = report.page_size
            page_number = report.page_number
            has_next_page = report.has_next_page
            rows.extend(report.result_table)
            cur_page += 1
        return report.column_list, rows
