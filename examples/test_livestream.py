# Demo to access livestream data for the user's specified event
#
# How to run
# python test_livestream.py --event_name=<YOUR_EVENT_NAME> --app_id=<APP ID> --api_uri=<API_URI> --ws_uri=<WEBSOCKET_URI> --username=<USERNAME> --password=<PASSWORD>
#
#
# Operation flow
#
# Login
# Fetch my most recent events
# Find specific event matching specified name
# Get eventdevices for the event
# request live sensor data for each eventdevice in event
# print out live sensor data for each eventdevice
#
# To test:
# * Ensure your device is not currently broadcast real-time data (to prevent it from auto-creating an ad-hoc event)
# * Create an event with a specified name - e.g. "my_event", with a date range that encompasses the current date (now)
# * Add your device to this event
# * Enable your device to broadcast real-time data
# * Launch this script with the appropriate parameters
#
# Note - If an ad-hoc event was already created, you can simply rename the event to your preferred name, and adjust the start / end
# times as necessary

import argparse
from time import sleep

from podium_api import register_podium_application
from podium_api.api import PodiumAPI
from podium_api.asyncreq import get_json_header_token
from podium_api.events import make_events_get
from podium_api.livestream import PodiumLivestream
from podium_api.login import make_login_post
from podium_api.types.account import PodiumAccount
from podium_api.types.event import PodiumEvent
from podium_api.types.user import PodiumUser


def parse_args():
    parser = argparse.ArgumentParser(description="Parse app connection parameters.")
    parser.add_argument("--event_name", required=True, help="Application ID")
    parser.add_argument("--app_id", required=True, help="Application ID")
    parser.add_argument("--api_uri", required=True, help="Application API URI")
    parser.add_argument("--ws_uri", required=True, help="WebSocket API URI")
    parser.add_argument("--username", required=True, help="Username")
    parser.add_argument("--password", required=True, help="Password")
    return parser.parse_args()


args = parse_args()


class Connection(object):
    def __init__(self, token, podium, account, user, livestream):
        self.token = token
        self.podium = podium
        self.account = account
        self.user = user
        self.livestream = livestream


class LivestreamTester:
    def __init__(self):
        self.connection = None

    def _on_connection_open(self):
        print("Websocket connection opened")

    def _on_connection_close(self):
        print("Websocket connection closed")

    def _sensor_data_listener(self, data):
        print(f"sensor data {data}")

    def _start_livestream_connection(self, token: str):
        print("Starting livestream connection")
        livestream = PodiumLivestream()
        livestream.set_connection_open_listener(self._on_connection_open)
        livestream.set_connection_close_listener(self._on_connection_close)
        livestream.set_sensor_data_listener(self._sensor_data_listener)
        header = get_json_header_token(token)
        livestream.open_connection(args.ws_uri, header)
        return livestream

    def _init_connection(self, token: str):
        def _success(account: PodiumAccount, user: PodiumUser):
            print(f"Init connection success")
            livestream = self._start_livestream_connection(token)
            self.connection = Connection(token=token, podium=podium, account=account, user=user, livestream=livestream)

        def _failure(error_type, results, data):
            print(f"Podium API init failure! error_type: {error_type}; results: {results}; data: {data}")

        self._podium = podium = PodiumAPI(token)
        podium.init_connection(success_callback=_success, failure_callback=_failure)

    def login(self):
        def _success(token: str):
            print(f"Login success")
            self._init_connection(token)

        def _failure(error_type, results, data):
            print(f"login failed! error_type: {error_type}; results: {results}; data: {data}")

        register_podium_application(args.app_id, "", args.api_uri)
        make_login_post(args.username, args.password, success_callback=_success, failure_callback=_failure)

    def get_event_for_name(self, event_name: str, callback):
        uri = f"{args.api_uri}/api/v1/account/events"

        def _success(paged_response):
            print(f"make_events_get success - got {len(paged_response.events)} results matching {event_name}")
            for event in paged_response.events:
                print(f"Picking the first matched event ({event.title})")
                callback(event)

        def _failure(error_type, results, data):
            print(f"Events failed! error_type: {error_type}; results: {results}; data: {data}")

        make_events_get(
            self.connection.token,
            endpoint=uri,
            success_callback=_success,
            failure_callback=_failure,
            title=event_name,
        )

    def register_sensordata_for_event(self, event: PodiumEvent):
        def _success(paged_response):
            print(f"Got eventdevices for event {event.title}")
            for eventdevice in paged_response.eventdevices:
                eventdevice_id = eventdevice.eventdevice_id
                print(f"Registering sensor data for eventdevice_id {eventdevice_id}")
                self.connection.livestream.register_sensor_data(eventdevice_id)

        def _failure(error_type, results, data):
            print(f"Eventdevices failed! error_type: {error_type}; results: {results}; data: {data}")

        self.connection.podium.eventdevices.list(
            endpoint=event.devices_uri,
            success_callback=_success,
            failure_callback=_failure,
        )


if __name__ == "__main__":

    def got_event_callback(event: PodiumEvent):
        print(f"Got event {event.title}, registering sensordata for each eventdevice")
        tester.register_sensordata_for_event(event)

    tester = LivestreamTester()
    tester.login()

    # wait for connection initialization
    while not tester.connection:
        sleep(1)
        tester.get_event_for_name(args.event_name, got_event_callback)

    while True:
        sleep(1)
