#!/usr/bin/env python
# -*- coding: utf-8 -*-
class PodiumRating(object):
    """
    Object that represents a Preset.

    **Attributes:**
        **preset_id** (int): Unique id for preset

        **uri** (str): Endpoint for accessing full preset information.

        **name** (str): Name of the preset.

        **notes** (str): Notes for this preset

        **preset** (str): JSON data for preset

        **mapping_type_id** (int): ID of the mapping type

        **mapping_type** (str): string key representation of the mapping type

        **updated** (str): Date preset was updated. ISO 8601 format.

        **created** (str): Date preset was created. ISO 8601 format.
    """

    def __init__(self, user_id, rating):
        self.rating = rating

def get_rating_from_json(json):
    """
    Returns a PodiumEvent object from the json dict received from podium api.

    Args:
        json (dict): Dict of data from REST api

    Return:
        PodiumEvent: The PodiumEvent object for this data.
    """
    return PodiumRating(json['rating'])
