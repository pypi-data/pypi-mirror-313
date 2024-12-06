from datetime import date, timedelta
import json
import pytest

import httpretty

from swiftly_api_client import (
    SwiftlyAPIClient,
    SwiftlyAPIClientError,
    SwiftlyAPIServerError,
)
from swiftly_api_client.network import configure_requests_session


@httpretty.activate
def test_handle_client_error():
    agency = "test_agency"
    route_name = "test_route"
    path = f"/run-times/{agency}/route/{route_name}/by-trip"
    url = SwiftlyAPIClient.PROD_BASE_URL + path

    target_date = date.today()

    expected_response = {"errorCode": 403, "errorMessage": "Permission Denied"}

    httpretty.register_uri(
        httpretty.GET,
        url,
        responses=[
            httpretty.Response(
                body=json.dumps(expected_response),
                status=403,
            ),
        ],
    )

    client = SwiftlyAPIClient(agency_key="test_agency", api_key="test_api_key")

    with pytest.raises(SwiftlyAPIClientError):
        client.get_runtimes_for_route_by_trip(
            route_short_name="test_route", start_date=target_date
        )


@httpretty.activate
def test_handle_server_error():
    agency = "test_agency"
    route_name = "test_route"
    path = f"/run-times/{agency}/route/{route_name}/by-trip"
    url = SwiftlyAPIClient.PROD_BASE_URL + path

    target_date = date.today()

    expected_response = {"errorCode": 500, "errorMessage": "Server Error"}

    session = configure_requests_session(retries=2, backoff_factor=0.0)

    httpretty.register_uri(
        httpretty.GET,
        url,
        responses=[
            httpretty.Response(
                body=json.dumps(expected_response),
                status=500,
            ),
            httpretty.Response(
                body=json.dumps(expected_response),
                status=500,
            ),
            httpretty.Response(
                body=json.dumps(expected_response),
                status=500,
            ),
        ],
    )

    client = SwiftlyAPIClient(
        agency_key="test_agency", api_key="test_api_key", session=session
    )

    with pytest.raises(SwiftlyAPIServerError):
        client.get_runtimes_for_route_by_trip(
            route_short_name="test_route", start_date=target_date
        )


@httpretty.activate
def test_get_runtimes_for_route_by_trip():
    agency = "test_agency"
    route_name = "test_route"
    path = f"/run-times/{agency}/route/{route_name}/by-trip"
    url = SwiftlyAPIClient.PROD_BASE_URL + path

    target_date = date.today()

    expected_response = {
        "route": path,
        "success": True,
        "result": {
            "direction-0": [
                {
                    "tripId": "test_trip_id",
                    "runtime": 12345,
                    "scheduledRuntime": 12345,
                    "scheduledDepartureSeconds": 600,
                    "timeFromStartUntilNextTrip": 54321,
                    "tripPattern": "gherogherog",
                    "firstStop": "test_first_stop",
                    "lastStop": "test_last_stop",
                    "observedRuntimes": [
                        {
                            "date": target_date.strftime("%m-%d-%Y"),
                            "dwellTime": 1000,
                            "travelTime": 2000,
                            "fixedTravel": 3000,
                            "runTime": 4000,
                            "vehicleId": "test_vehicle_id",
                        }
                    ],
                }
            ],
            "direction-1": [],
        },
    }

    httpretty.register_uri(
        httpretty.GET,
        url,
        responses=[
            httpretty.Response(
                body=json.dumps(expected_response),
                status=200,
            ),
        ],
    )

    client = SwiftlyAPIClient(agency_key="test_agency", api_key="test_api_key")

    runtimes_resp = client.get_runtimes_for_route_by_trip(
        route_short_name="test_route", start_date=target_date
    )

    assert runtimes_resp == expected_response["result"]

    sent_req = httpretty.last_request()
    assert sent_req.querystring["startDate"] == [target_date.strftime("%m-%d-%Y")]


@httpretty.activate
def test_get_runtimes_for_route_by_trip_with_multiple_dates():
    agency = "test_agency"
    route_name = "test_route"
    path = f"/run-times/{agency}/route/{route_name}/by-trip"
    url = SwiftlyAPIClient.PROD_BASE_URL + path

    target_date = date.today()
    target_date_2 = date.today() - timedelta(days=1)

    expected_response = {
        "route": path,
        "success": True,
        "result": {
            "direction-0": [
                {
                    "tripId": "test_trip_id",
                    "runtime": 12345,
                    "scheduledRuntime": 12345,
                    "scheduledDepartureSeconds": 600,
                    "timeFromStartUntilNextTrip": 54321,
                    "tripPattern": "gherogherog",
                    "firstStop": "test_first_stop",
                    "lastStop": "test_last_stop",
                    "observedRuntimes": [
                        {
                            "date": target_date_2.strftime("%m-%d-%Y"),
                            "dwellTime": 1000,
                            "travelTime": 2000,
                            "fixedTravel": 3000,
                            "runTime": 4000,
                            "vehicleId": "test_vehicle_id",
                        },
                        {
                            "date": target_date.strftime("%m-%d-%Y"),
                            "dwellTime": 1000,
                            "travelTime": 2000,
                            "fixedTravel": 3000,
                            "runTime": 4000,
                            "vehicleId": "test_vehicle_id",
                        },
                    ],
                }
            ],
            "direction-1": [],
        },
    }

    httpretty.register_uri(
        httpretty.GET,
        url,
        responses=[
            httpretty.Response(
                body=json.dumps(expected_response),
                status=200,
            ),
        ],
    )

    client = SwiftlyAPIClient(agency_key=agency, api_key="test_api_key")

    runtimes_resp = client.get_runtimes_for_route_by_trip(
        route_short_name="test_route", start_date=target_date
    )

    assert runtimes_resp == expected_response["result"]


@httpretty.activate
def test_get_on_time_performance_export():
    agency = "test_agency"
    target_date = date(2020, 12, 21)
    client = SwiftlyAPIClient(agency_key=agency, api_key="test_api_key")

    path = f"/otp/{agency}/csv-export"
    url = SwiftlyAPIClient.PROD_BASE_URL + path

    with open("tests/fixtures/nctd_swiftly_otp_export_2020-12-21.csv", "r") as f:
        httpretty.register_uri(
            httpretty.GET,
            url,
            responses=[
                httpretty.Response(
                    body=f.read(),
                    status=200,
                ),
            ],
        )
        df = client.get_on_time_performance_export(
            start_date=target_date,
            end_date=target_date,
            days_of_week=[1, 2, 3, 4, 5],
            exclude_dates=[
                target_date + timedelta(days=1),
                target_date + timedelta(days=2),
            ],
            use_service_dates=False,
            only_first_stop_of_trip=True,
        )
        assert (
            df[df["trip_id"] == "15141675-NC2010-NCTD-Weekday-06"].iloc[0].block_id
            == 30102
        )
        assert (
            df[df["trip_id"] == "15141699-NC2010-NCTD-Weekday-06"].iloc[0].block_id
            == 30106
        )
        assert (
            df[df["trip_id"] == "15141691-NC2010-NCTD-Weekday-06"].iloc[0].block_id
            == 30104
        )

    sent_req = httpretty.last_request()
    assert sent_req.querystring["startDate"] == ["12-21-2020"]
    assert sent_req.querystring["endDate"] == ["12-21-2020"]
    assert sent_req.querystring["daysOfWeek"] == ["1,2,3,4,5"]
    assert sent_req.querystring["excludeDates"] == ["12-22-2020,12-23-2020"]
    assert sent_req.querystring["useServiceDates"] == ["false"]
    assert sent_req.querystring["onlyFirstStopOfTrip"] == ["true"]


@httpretty.activate
def test_get_trip_observations_export():
    agency = "test_agency"
    target_date = date(2023, 6, 30)
    client = SwiftlyAPIClient(agency_key=agency, api_key="test_api_key")

    path = f"/run-times/{agency}/trip-observations"
    url = SwiftlyAPIClient.PROD_BASE_URL + path

    with open(
        "tests/fixtures/rtacm_swiftly_trip_observations_export_2023-06-30.csv", "r"
    ) as f:
        httpretty.register_uri(
            httpretty.GET,
            url,
            responses=[
                httpretty.Response(
                    body=f.read(),
                    status=200,
                ),
            ],
        )
        df = client.get_trip_observations_export(
            start_date=target_date,
            end_date=target_date,
            days_of_week=[1, 2, 3, 4, 6, 7],
            exclude_dates=[
                target_date + timedelta(days=1),
                target_date + timedelta(days=2),
            ],
        )
        assert (
            df[df["tripId"] == "t_5561911_b_80157_tn_0"].iloc[0].scheduleRelationship
            == "SCHEDULED"
        )
        assert (
            df[df["tripId"] == "t_5561915_b_80157_tn_11"].iloc[0].scheduleRelationship
            == "CANCELED"
        )

    sent_req = httpretty.last_request()
    assert sent_req.querystring["startDate"] == ["06-30-2023"]
    assert sent_req.querystring["endDate"] == ["06-30-2023"]
    assert sent_req.querystring["daysOfWeek"] == ["1,2,3,4,6,7"]
    assert sent_req.querystring["excludeDates"] == ["07-01-2023,07-02-2023"]


@httpretty.activate
def test_get_trip_observations_export_empty():
    agency = "test_agency"
    target_date = date(2023, 6, 30)
    client = SwiftlyAPIClient(agency_key=agency, api_key="test_api_key")

    path = f"/run-times/{agency}/trip-observations"
    url = SwiftlyAPIClient.PROD_BASE_URL + path

    with open(
        "tests/fixtures/rtacm_swiftly_trip_observations_export_empty.csv", "r"
    ) as f:
        httpretty.register_uri(
            httpretty.GET,
            url,
            responses=[
                httpretty.Response(
                    body=f.read(),
                    status=200,
                ),
            ],
        )
        df = client.get_trip_observations_export(
            start_date=target_date,
            end_date=target_date,
            days_of_week=[1, 2, 3, 4, 6, 7],
            exclude_dates=[
                target_date + timedelta(days=1),
                target_date + timedelta(days=2),
            ],
        )
        assert df.empty

    sent_req = httpretty.last_request()
    assert sent_req.querystring["startDate"] == ["06-30-2023"]
    assert sent_req.querystring["endDate"] == ["06-30-2023"]
    assert sent_req.querystring["daysOfWeek"] == ["1,2,3,4,6,7"]
    assert sent_req.querystring["excludeDates"] == ["07-01-2023,07-02-2023"]


@httpretty.activate
def test_get_raw_apc_events():
    agency = "test_agency"
    target_date = date(2023, 10, 1)
    client = SwiftlyAPIClient(agency_key=agency, api_key="test_api_key")

    path = f"/ridership/{agency}/apc-raw-events"
    url = SwiftlyAPIClient.PROD_BASE_URL + path

    httpretty.register_uri(
        httpretty.GET,
        url,
        responses=[
            httpretty.Response(
                body="""
                {
                    "apcRawEvents": [
                        {
                            "id": 21293621,
                            "vehicle_id": "2203",
                            "time": "2023-10-01 08:16:56.997",
                            "latitude": 39.128956,
                            "longitude": -76.803697,
                            "ons": 0,
                            "offs": 0
                        },
                        {
                            "id": 21293622,
                            "vehicle_id": "2203",
                            "time": "2023-10-01 08:16:57.006",
                            "latitude": 39.128956,
                            "longitude": -76.803697,
                            "ons": 0,
                            "offs": 0
                        }
                    ]
                }
                """,
                status=200,
            ),
        ],
    )
    data = client.get_raw_apc_events(target_date)

    assert data == [
        {
            "id": 21293621,
            "vehicle_id": "2203",
            "time": "2023-10-01 08:16:56.997",
            "latitude": 39.128956,
            "longitude": -76.803697,
            "ons": 0,
            "offs": 0,
        },
        {
            "id": 21293622,
            "vehicle_id": "2203",
            "time": "2023-10-01 08:16:57.006",
            "latitude": 39.128956,
            "longitude": -76.803697,
            "ons": 0,
            "offs": 0,
        },
    ]

    sent_req = httpretty.last_request()
    assert sent_req.querystring["date"] == ["2023-10-01"]


@httpretty.activate
def test_get_arrivals_departures_observations_invalid_date_range():
    agency = "test_agency"
    target_date = date(2023, 10, 1)
    client = SwiftlyAPIClient(agency_key=agency, api_key="test_api_key")

    path = f"/otp/{agency}/arrivals-departures"
    url = SwiftlyAPIClient.PROD_BASE_URL + path

    httpretty.register_uri(
        httpretty.GET,
        url,
        responses=[
            httpretty.Response(
                body="""
                {
                    "errorCode":404,
                    "errorMessage":"Data is not available for the requested date range from this endpoint.
                    Try using the By Schedule endpoint instead."
                }""",
                status=404,
            ),
        ],
    )

    df = client.get_arrivals_departures_observations(target_date)

    assert df.empty
