#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kivy.app import App
from podium_api import register_podium_application
from podium_api.login import make_login_post
from podium_api.users import make_user_get
from podium_api.account import make_account_get
from podium_api.events import (
    make_events_get, make_event_create, make_event_get, make_event_delete,
    make_event_update
    )
from podium_api.types.token import PodiumToken
from plyer import keystore
from datetime import date

APP_ID = "00833f5ab53d1f696735793f5fac320de0211ccf231b35c447562066e97caaaf"
APP_SECRET = "eda2bdee04abfa484688c77a0e438cad2dfa6eef07879a24cb102d85c9da2674"

TOKEN = None

class NoStoredToken(Exception):
    pass

class PodiumApp(App):

    def on_start(self):
        register_podium_application(APP_ID, APP_SECRET)
        email = "kovac1066@gmail.com" #put a username here
        secret = "zaeron19" #put a password here
        req = make_login_post(email, secret,
                              success_callback=self.login_success,
                              failure_callback=self.failure,
                              progress_callback=self.progress)


    def account_success(self, account):
        # make_events_get(TOKEN, endpoint=account.events_uri,
        #                 success_callback=self.events_success,
        #                 failure_callback=self.failure,
        #                 progress_callback=self.progress)
        make_event_create(TOKEN, "test event", date(2016, 6, 27).isoformat(),
                          date(2016, 6, 28).isoformat(),
                          redirect_callback=self.create_success,
                          failure_callback=self.failure,
                          progress_callback=self.progress)

    def event_update_success(self, server_message, event_uri):
        print(server_message, event_uri)
        make_event_get(TOKEN, event_uri,
                       success_callback=self.event_get_success,
                       failure_callback=self.failure,
                       progress_callback=self.progress)

    def create_success(self, redirect_object):
        print("redirect after create", redirect_object.__dict__)
        make_event_update(TOKEN, redirect_object.location,
                          title="new_title",
                          success_callback=self.event_update_success,
                          failure_callback=self.failure,
                          progress_callback=self.progress)


    def delete_success(self, deleted_uri):
        print(deleted_uri, " was deleted")

    def event_get_success(self, event):
        print(event.title)
        make_event_delete(TOKEN, event.uri,
                          success_callback=self.delete_success,
                          failure_callback=self.failure,
                          progress_callback=self.progress)

    def store_token(self, token):
        #example of fully serializing a token
        keystore.set_key("autosportslabs.podium_api.test",
                         "token", token.token)
        keystore.set_key("autosportslabs.podium_api.test",
                         "token_type", token.token_type)
        keystore.set_key("autosportslabs.podium_api.test",
                         "token_created", str(token.created))

    def load_token(self):
        #example of restoring a token entirely
        token = keystore.get_key("autosportslabs.podium_api.test", "token")
        token_type = keystore.get_key("autosportslabs.podium_api.test",
                                      "token_type")
        created = keystore.get_key("autosportslabs.podium_api.test",
                                   "token_created")
        if token is None or token_type is None or created is None:
            raise NoStoredToken()
        return PodiumToken(token, token_type, int(created))

    def events_success(self, paged_response):
        print(paged_response, len(paged_response.events))
        if paged_response.next_uri is not None:
            make_events_get(TOKEN, endpoint=paged_response.next_uri,
                            success_callback=self.events_success,
                            failure_callback=self.failure,
                            progress_callback=self.progress)


    def users_success(self, user):
        print(user, user.__dict__)

    def login_success(self, token):
        #use plyer to save the token in crossplatform way
        self.store_token(token)
        global TOKEN
        TOKEN = self.load_token()
        make_account_get(token,
                         success_callback=self.account_success,
                         failure_callback=self.failure,
                         progress_callback=self.progress)

    def failure(self, error_type, results, data):
        #handle errors
        print(error_type, results)

    def progress(self, current_size, total_size, data):
        #handle updating progress visually
        print(current_size, total_size)

if __name__ == '__main__':
    PodiumApp().run()
