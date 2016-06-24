#!/usr/bin/env python
# -*- coding: utf-8 -*-

class PodiumUser(object):
    '''
    Object that represents a particular User.

    **Attributes:**
        **user_id** (int): User id

        **uri** (string): URI for the User.

        **username** (string): The User's username.

        **description** (string): The User's description.

        **avatar_url** (string): User's avatar image url.

        **links** (list): 3rd party links for the user.

        **friendships_uri** (string): URI to friends list.

        **followers_uri** (string): URI to followers list.
    '''

    def __init__(self, user_id, uri, username, description, avatar_url,
                 links, friendships_uri, followers_uri):
        self.user_id = user_id
        self.uri = uri
        self.username = username
        self.description = description
        self.avatar_url = avatar_url
        self.links = links
        self.friendships_uri = friendships_uri
        self.followers_uri = followers_uri
