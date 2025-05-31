import argparse
from time import sleep

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from podium_api import register_podium_application
from podium_api.asyncreq import get_json_header_token
from podium_api.livestream import PodiumLivestream
from podium_api.login import make_login_post


def parse_args():
    parser = argparse.ArgumentParser(description="Parse app connection parameters.")
    parser.add_argument("--app_id", required=True, help="Application ID")
    parser.add_argument("--api_uri", required=True, help="Application API URI")
    parser.add_argument("--ws_uri", required=True, help="WebSocket API URI")
    parser.add_argument("--username", required=True, help="Username")
    parser.add_argument("--password", required=True, help="Password")
    return parser.parse_args()


args = parse_args()

KV = """
<MyWidget>:
    orientation: 'vertical'
    spacing: 10
    padding: 10

    TextInput:
        id: text_box
        text: ""
        multiline: True
        size_hint_y: 0.9

    Button:
        text: "Start"
        size_hint_y: 0.1
        on_press: app.on_button_click()
"""


class MyWidget(BoxLayout):
    pass


class MyApp(App):
    def build(self):
        Builder.load_string(KV)
        return MyWidget()

    def on_connection_open(self):
        print("connection opened")
        self._livestream.list_telemetry_sessions()

    def on_connection_close(self):
        print("connection closed")

    def on_list_telemetry_sessions(self, body):
        print(f"telemetry sessions: {body}")
        
    def start_livestream(self, token):
        self._livestream = livestream = PodiumLivestream()
        livestream.set_connection_open_listener(self.on_connection_open)
        livestream.set_connection_close_listener(self.on_connection_close)
        livestream.set_list_telemetry_sessions_listener(self.on_list_telemetry_sessions)

        header = get_json_header_token(token)
        livestream.open_connection(args.ws_uri, header)

    def login_success(self, token):
        print(f"login success: {token}")
        self.start_livestream(token)

    def login_failure(self, error_type, results, data):
        print(f"login failed! error_type: {error_type}; results: {results}; data: {data}")

    def login(self):
        register_podium_application(args.app_id, "", args.api_uri)

        make_login_post(
            args.username, args.password, success_callback=self.login_success, failure_callback=self.login_failure
        )

    def on_button_click(self):
        self.login()


if __name__ == "__main__":
    MyApp().run()
