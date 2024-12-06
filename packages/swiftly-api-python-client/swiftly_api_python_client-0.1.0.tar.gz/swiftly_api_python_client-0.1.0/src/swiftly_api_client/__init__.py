import datetime
import io

from typing import Optional, Union

import pandas as pd

from requests import Session
from requests.exceptions import RetryError

from swiftly_api_client.network import configure_requests_session


class SwiftlyAPIClientError(Exception):
    pass


class SwiftlyAPIServerError(Exception):
    pass


class SwiftlyAPIClient:
    PROD_BASE_URL = "https://api.goswift.ly"

    RUN_TIMES_BY_ROUTE = "/run-times/{agency_key}/route/{route_short_name}/by-trip"
    OTP_EXPORT = "/otp/{agency_key}/csv-export"
    TRIP_OBSERVATIONS = "/run-times/{agency_key}/trip-observations"
    ARRIVAL_DEPARTURE_OBSERVATIONS = "/otp/{agency_key}/arrivals-departures"
    RAW_APC_EVENTS = "/ridership/{agency_key}/apc-raw-events"

    def __init__(
        self,
        agency_key: str,
        api_key: str,
        base_url: Optional[str] = None,
        session: Optional[Session] = None,
    ) -> None:
        self.agency_key = agency_key
        self.api_key = api_key
        self.base_url = base_url or self.PROD_BASE_URL
        self.session = session or configure_requests_session()
        self.headers = {"Authorization": api_key}

    def _build_default_query_params(
        self,
        start_date: datetime.date,
        end_date: Optional[datetime.date] = None,
        days_of_week: Optional[list[int]] = None,
        exclude_dates: Optional[list[datetime.date]] = None,
    ) -> dict:
        query_params = {
            "startDate": start_date.strftime("%m-%d-%Y"),
        }
        if end_date:
            query_params["endDate"] = end_date.strftime("%m-%d-%Y")
        if days_of_week:
            query_params["daysOfWeek"] = ",".join(map(str, days_of_week))
        if exclude_dates:
            query_params["excludeDates"] = ",".join(
                map(lambda d: d.strftime("%m-%d-%Y"), exclude_dates)
            )
        return query_params

    def _perform_request(
        self, url: str, query_params: dict, is_json: bool = True, data_key: str = "data"
    ) -> Union[dict, str, list[dict]]:
        """
        Send the prepared request to the server.

        :param url: The URL to send the request to.
        :param query_params: The query parameters to send with the request.
        :param is_json: Whether the response is JSON.
        :param data_key: The key to use for the data in the response. Only applicable if the response is JSON.

        Note: most api requests return the data in the key "data" but a handful use "result" instead.
        """
        try:
            response = self.session.get(url, params=query_params, headers=self.headers)
        except RetryError as e:
            raise SwiftlyAPIServerError(str(e))

        if 200 <= response.status_code < 300:
            if is_json:
                resp_dict = response.json()

                if (
                    "success" in resp_dict
                    and resp_dict["success"]
                    or "success" not in resp_dict
                ):
                    return resp_dict[data_key]
            else:
                return response.text

            raise SwiftlyAPIClientError("Swiftly API Body Status Error")
        elif 400 <= response.status_code < 500:
            raise SwiftlyAPIClientError(response.text)
        else:
            raise SwiftlyAPIServerError(response.text)

    def get_runtimes_for_route_by_trip(
        self,
        route_short_name: str,
        start_date: datetime.date,
        end_date: Optional[datetime.date] = None,
        days_of_week: Optional[list[int]] = None,
        exclude_dates: Optional[list[datetime.date]] = None,
    ) -> dict:
        """
        Get runtimes for a route by trip.

        https://dashboard.goswift.ly/nctd/api-guide/reference
        GET /run-times/{agencyKey}/route/{routeKey}/by-trip

        :param route_short_name: The route short name.
        :param start_date: The start date.
        :param end_date: The end date. If omitted, the end date is the start date so a single date is returned.
        :param days_of_week: The days of the week to return. If omitted, all days of the week are returned. Formatted
            as a list of isoweekdays, where 1 is Monday and 7 is Sunday.
        :param exclude_dates: The dates to exclude.
        :return: A dictionary of runtimes keyed by trip.
        """
        query_params = self._build_default_query_params(
            start_date=start_date,
            end_date=end_date,
            days_of_week=days_of_week,
            exclude_dates=exclude_dates,
        )

        url = self.base_url + self.RUN_TIMES_BY_ROUTE.format(
            agency_key=self.agency_key,
            route_short_name=route_short_name,
        )

        return self._perform_request(url, query_params, data_key="result")

    def get_on_time_performance_export(
        self,
        start_date: datetime.date,
        end_date: Optional[datetime.date] = None,
        days_of_week: Optional[list[int]] = None,
        exclude_dates: Optional[list[datetime.date]] = None,
        use_service_dates: Optional[bool] = None,
        only_first_stop_of_trip: Optional[bool] = None,
    ) -> pd.DataFrame:
        """
        Get runtimes for a route by trip.

        https://dashboard.goswift.ly/nctd/api-guide/reference
        GET /otp/{agencyKey}/csv-export

        :param start_date: The start date.
        :param end_date: The end date. If omitted, the end date is the start date so a single date is returned.
        :param days_of_week: The days of the week to return. If omitted, all days of the week are returned. Formatted
            as a list of isoweekdays, where 1 is Monday and 7 is Sunday.
        :param exclude_dates: The dates to exclude.
        :param only_first_stop_of_trip: If true, only the first stop of a trip is returned.
        :param use_service_dates: If true, the service dates are used trips/stops which occur after mightnight will
            be returned with a time > 24:00.
        :return: A pandas dataframe of the export.
        """
        query_params = self._build_default_query_params(
            start_date=start_date,
            end_date=end_date,
            days_of_week=days_of_week,
            exclude_dates=exclude_dates,
        )

        if only_first_stop_of_trip is not None:
            query_params["onlyFirstStopOfTrip"] = (
                "true" if only_first_stop_of_trip else "false"
            )

        if use_service_dates is not None:
            query_params["useServiceDates"] = "true" if use_service_dates else "false"

        url = self.base_url + self.OTP_EXPORT.format(agency_key=self.agency_key)

        resp = self._perform_request(url, query_params, is_json=False)

        try:
            df = pd.read_csv(io.StringIO(resp))
        except pd.errors.EmptyDataError:
            df = pd.DataFrame()
        return df

    def get_trip_observations_export(
        self,
        start_date: datetime.date,
        end_date: Optional[datetime.date] = None,
        days_of_week: Optional[list[int]] = None,
        exclude_dates: Optional[list[datetime.date]] = None,
    ) -> pd.DataFrame:
        """
        Get trip observations aka what actually happened on the ground

        https://dashboard.goswift.ly/nctd/api-guide/reference
        GET /run-times/{agencyKey}/trip-observations

        :param start_date: The start date.
        :param end_date: The end date. If omitted, the end date is the start date so a single date is returned.
        :param days_of_week: The days of the week to return. If omitted, all days of the week are returned. Formatted
            as a list of isoweekdays, where 1 is Monday and 7 is Sunday.
        :param exclude_dates: The dates to exclude.
        :param use_service_dates: If true, the service dates are used trips/stops which occur after mightnight will
            be returned with a time > 24:00.
        :return: A pandas dataframe of the export.
        """
        query_params = self._build_default_query_params(
            start_date=start_date,
            end_date=end_date,
            days_of_week=days_of_week,
            exclude_dates=exclude_dates,
        )

        query_params["format"] = "csv"

        url = self.base_url + self.TRIP_OBSERVATIONS.format(agency_key=self.agency_key)

        resp = self._perform_request(url, query_params, is_json=False)

        try:
            df = pd.read_csv(io.StringIO(resp))
        except pd.errors.EmptyDataError:
            df = pd.DataFrame()
        return df

    def get_arrivals_departures_observations(
        self,
        start_date: datetime.date,
        end_date: Optional[datetime.date] = None,
        days_of_week: Optional[list[int]] = None,
        exclude_dates: Optional[list[datetime.date]] = None,
    ) -> pd.DataFrame:
        """
        Provides information about scheduled and observed arrivals and departures for specified route(s).
        The returned data is an array of arrival and departure observations that include scheduled times,
        and, if available, observed timing.

        https://dashboard.goswift.ly/nctd/api-guide/reference
        GET /run-times/{agencyKey}/trip-observations

        :param start_date: The start date.
        :param end_date: The end date. If omitted, the end date is the start date so a single date is returned.
        :param days_of_week: The days of the week to return. If omitted, all days of the week are returned. Formatted
            as a list of isoweekdays, where 1 is Monday and 7 is Sunday.
        :param exclude_dates: The dates to exclude.
        :return: A pandas dataframe of the export.
        """
        query_params = self._build_default_query_params(
            start_date=start_date,
            end_date=end_date,
            days_of_week=days_of_week,
            exclude_dates=exclude_dates,
        )

        query_params["format"] = "csv"

        url = self.base_url + self.ARRIVAL_DEPARTURE_OBSERVATIONS.format(
            agency_key=self.agency_key
        )

        try:
            resp = self._perform_request(url, query_params, is_json=False)
        except SwiftlyAPIClientError as e:
            if (
                "Data is not available for the requested date range from this endpoint"
                in str(e)
            ):
                return pd.DataFrame()

        try:
            df = pd.read_csv(io.StringIO(resp))
        except pd.errors.EmptyDataError:
            df = pd.DataFrame()
        return df

    def get_raw_apc_events(
        self,
        date_to_fetch: datetime.date,
    ) -> list[dict]:
        """
        Provides unprocessed APC data points (door open/close events), complemented with the inferred
        latitude/longitude of the vehicle. Returns data for one calendar date at a time, i.e. it does not
        follow the GTFS service-dates concept, but instead goes from midnight to midnight on the specified
        calendar date.

        https://dashboard.goswift.ly/nctd/api-guide/reference
        GET /ridership/{agencyKey}/apc-raw-events

        :param date_to_fetch: The calendar date to fetch.
        :return: A list of dictionaries of the raw APC events.
        """
        query_params = {"date": date_to_fetch.isoformat()}

        url = self.base_url + self.RAW_APC_EVENTS.format(agency_key=self.agency_key)

        return self._perform_request(
            url, query_params, is_json=True, data_key="apcRawEvents"
        )
