#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import date

from kivy.app import App
from plyer import keystore

from podium_api import register_podium_application
from podium_api.account import make_account_get
from podium_api.api import PodiumAPI
from podium_api.events import (
    make_event_create,
    make_event_delete,
    make_event_get,
    make_event_update,
    make_events_get,
)
from podium_api.friendships import (
    make_friendship_create,
    make_friendship_delete,
    make_friendship_get,
    make_friendships_get,
)
from podium_api.login import make_login_post
from podium_api.types.token import PodiumToken
from podium_api.users import make_user_get

APP_ID = "YOUR_ID_HERE"
APP_SECRET = "YOUR_SECRET_HERE"


class NoStoredToken(Exception):
    pass


class PodiumApp(App):
    def on_start(self):
        register_podium_application(APP_ID, APP_SECRET)
        email = ""  # put a username here
        secret = ""  # put a password here
        self.events = []
        self.devices = []
        req = make_login_post(
            email,
            secret,
            success_callback=self.login_success,
            failure_callback=self.failure,
            progress_callback=self.progress,
        )

    def login_success(self, token):
        # use plyer to save the token in crossplatform way
        self.store_token(token)
        self.podium = podium = PodiumAPI(token)
        self.token = token
        podium.account.get(
            success_callback=self.account_success, failure_callback=self.failure, progress_callback=self.progress
        )

    def create_eventdevice_for_event(self):
        event = self.events[0]
        device = self.devices[1]
        print(event.__dict__)
        print(device.__dict__)
        self.podium.eventdevices.create(
            event.event_id,
            device.device_id,
            "test name",
            redirect_callback=self.eventdevices_success,
            failure_callback=self.failure,
        )

        # podium.eventdevices.create()

    def eventdevices_success(self, redirect):
        print("event device created", redirect.__dict__)

    def user_success(self, user):
        print(user.__dict__)
        self.user = user
        # self.podium.events.get(endpoint=user.events_uri)
        # make_friendships_get(self.token, user.friendships_uri,
        #                      success_callback=self.friendship_success)

    def friendship_success2(self, paged_response):
        print(paged_response.__dict__)

    def devices_success(self, paged_response):
        print("devices")
        print(paged_response.__dict__)
        self.devices += paged_response.devices
        if paged_response.next_uri is not None:
            self.podium.devices.list(paged_response.next_uri, success_callback=self.devices_success)
        else:
            self.create_eventdevice_for_event()

    def friendship_success(self, paged_response):
        print(paged_response.__dict__)
        # make_friendship_delete(self.token,
        #                        paged_response.users[0].friendship_uri)
        # make_friendships_get(self.token, self.user.friendships_uri,
        #                      success_callback=self.friendship_success2)

    def friendship_redirect(self, redirect):
        make_friendship_get(self.token, redirect.location, success_callback=self.users_success)

    def account_success(self, account):
        # make_friendship_create(self.token, 22,
        #                        redirect_callback=self.friendship_redirect)
        self.account = account
        self.podium.users.get(endpoint=account.user_uri, success_callback=self.user_success)
        self.podium.events.list(
            endpoint=account.events_uri,
            success_callback=self.events_success,
            failure_callback=self.failure,
            progress_callback=self.progress,
        )
        self.podium.events.create(
            "test event",
            date(2016, 6, 27).isoformat(),
            date(2016, 6, 28).isoformat(),
            redirect_callback=self.create_success,
            failure_callback=self.failure,
            progress_callback=self.progress,
        )
        self.podium.devices.create(
            "test device",
            redirect_callback=self.create_device_success,
            failure_callback=self.failure,
            progress_callback=self.progress,
        )

    def device_success(self, device):
        print(device, device.__dict__)
        self.podium.devices.update(
            device.uri,
            name="new name",
            success_callback=self.device_update_success,
        )

    def device_update_success(self, message, update_uri):
        print(message, update_uri)
        self.podium.devices.delete(
            update_uri, success_callback=self.success, failure_callback=self.failure, progress_callback=self.progress
        )

    def create_device_success(self, redirect_object):
        print("getting device")
        self.podium.devices.get(
            redirect_object.location,
            success_callback=self.device_success,
            failure_callback=self.failure,
            progress_callback=self.progress,
        )

    def create_success(self, redirect_object):
        print("redirect after create", redirect_object.__dict__)
        self.podium.events.update(
            redirect_object.location,
            title="new_title",
            success_callback=self.event_update_success,
            failure_callback=self.failure,
            progress_callback=self.progress,
        )

    def event_update_success(self, server_message, event_uri):
        print(server_message, event_uri)
        self.podium.events.get(
            event_uri,
            success_callback=self.event_get_success,
            failure_callback=self.failure,
            progress_callback=self.progress,
        )

    def event_get_success(self, event):
        print(event.title)
        self.podium.events.delete(
            event.uri,
            success_callback=self.delete_success,
            failure_callback=self.failure,
            progress_callback=self.progress,
        )

    def delete_success(self, deleted_uri):
        print(deleted_uri, " was deleted")

    def store_token(self, token):
        # example of fully serializing a token
        keystore.set_key("autosportslabs.podium_api.test", "token", token.token)
        keystore.set_key("autosportslabs.podium_api.test", "token_type", token.token_type)
        keystore.set_key("autosportslabs.podium_api.test", "token_created", str(token.created))

    def load_token(self):
        # example of restoring a token entirely
        token = keystore.get_key("autosportslabs.podium_api.test", "token")
        token_type = keystore.get_key("autosportslabs.podium_api.test", "token_type")
        created = keystore.get_key("autosportslabs.podium_api.test", "token_created")
        if token is None or token_type is None or created is None:
            raise NoStoredToken()
        return PodiumToken(token, token_type, int(created))

    def events_success(self, paged_response):
        print(paged_response, len(paged_response.events))
        self.events += paged_response.events
        if paged_response.next_uri is not None:
            make_events_get(
                self.token,
                endpoint=paged_response.next_uri,
                success_callback=self.events_success,
                failure_callback=self.failure,
                progress_callback=self.progress,
            )
        else:
            self.podium.devices.list(self.account.devices_uri, success_callback=self.devices_success)

    def users_success(self, user):
        print(user, user.__dict__)

    def success(self, result):
        print(result)

    def failure(self, error_type, results, data):
        # handle errors
        print(error_type, results)

    def progress(self, current_size, total_size, data):
        # handle updating progress visually
        print(current_size, total_size)


if __name__ == "__main__":
    PodiumApp().run()
