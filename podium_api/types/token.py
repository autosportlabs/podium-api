#!/usr/bin/env python
# -*- coding: utf-8 -*-

class PodiumToken(object):
    '''
    A PodiumToken holds the OAuth2 Token for a logged in user.

    **Attributes:**
        **token** (string): The OAuth2 token for the user.

        **token_type** (string): The type of token issued.

        **created** (int): The time created.register_podium_application.
    '''

    def __init__(self, token, token_type, created):
        self.token = token
        self.token_type = token_type
        self.created = created
