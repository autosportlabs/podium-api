#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kivy.app import App
from podium_api import register_podium_application
from podium_api.login import make_login_request

APP_ID = "00833f5ab53d1f696735793f5fac320de0211ccf231b35c447562066e97caaaf"
APP_SECRET = "eda2bdee04abfa484688c77a0e438cad2dfa6eef07879a24cb102d85c9da2674"

class PodiumApp(App):

    def on_start(self):
        register_podium_application(APP_ID, APP_SECRET)
        email = "" #put a username here
        secret = "" #put a password here
        req = make_login_request(email, secret,
                                 success_callback=self.login_success,
                                 failure_callback=self.login_failure,
                                 progress_callback=self.login_progress)


    def login_success(self, token):
        #do what you want with the token
        print(token, token.token, token.created)

    def login_failure(self, error_type, results, data):
        #handle errors
        print(error_type, results)

    def login_progress(self, current_size, total_size, data):
        #handle updating progress visually
        print(current_size, total_size)

if __name__ == '__main__':
    PodiumApp().run()