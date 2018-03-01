#!/usr/bin/env python
# -*- coding: utf-8 -*-

class PodiumVenue(object):
    """
    Object that represents a Venue.

    **Attributes:**
        **venue_id** (int): Venue Id

        **uri** (string): URI for the Venue.

        **name** (string): The Venue's name.
    """
    def __init__(self, venue_id, uri, name):
        self.venue_id = venue_id
        self.uri = uri
        self.name = name


def get_venue_from_json(json):
    """
    Returns a PodiumVenue object from the json dict received from podium api.

    Args:
        json (dict): Dict of data from REST api

    Return:
        PodiumVenue: The PodiumVenue object for the data.
    """
    return PodiumVenue(json['id'],
                      json['URI'],
                      'name'
                      )
