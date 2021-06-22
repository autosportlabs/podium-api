#!/usr/bin/env python
# -*- coding: utf-8 -*-
class PodiumPreset(object):
    """
    Object that represents a Preset.

    **Attributes:**
        **preset_id** (int): Unique id for preset

        **uri** (str): Endpoint for accessing full preset information.

        **name** (str): Name of the preset.

        **notes** (str): Notes for this preset

        **preset** (str): JSON data for preset

        **type** (int): mapping type key

        **mapping_type** (str): string key representation of the mapping type

        **updated** (str): Date preset was updated. ISO 8601 format.

        **created** (str): Date preset was created. ISO 8601 format.
    """
    MAPPING_TYPE_ANALOG = "analog"
    MAPPING_TYPE_CAN = "can"
    MAPPING_TYPE_OBDII = "obd2"
    MAPPING_TYPE_PODIUM_DASH = "podium_dash"
    MAPPING_TYPE_PODIUM_CONNECT = "PC"
    MAPPING_TYPE_RACECAPTURE_ANALYSIS = "rc_analysis"
    MAPPING_TYPE_RACECAPTURE_PRO = "RCP"
    MAPPING_TYPE_RACECAPTURE_TRACK = "RCT"
    MAPPING_TYPE_RACECAPTURE_DASH = "rc_dash"
    MAPPING_TYPE_SCRIPTING = "Script"

    def __init__(self, preset_id, uri, name, notes, preset_data, type, private, rating, rating_count, user_uri, preview_image_url, updated, created):
        self.preset_id = preset_id
        self.uri = uri
        self.name = name
        self.notes = notes
        self.preset_data = preset_data
        self.type = type
        self.private = private
        self.rating = rating
        self.rating_count = rating_count
        self.user_uri = user_uri
        self.preview_image_url = preview_image_url
        self.updated = updated
        self.created = created

def get_preset_from_json(json):
    """
    Returns a PodiumEvent object from the json dict received from podium api.

    Args:
        json (dict): Dict of data from REST api

    Return:
        PodiumEvent: The PodiumEvent object for this data.
    """
    return PodiumPreset(json['id'],
                        json['URI'],
                       json.get('name', None),
                       json.get('notes', None),
                       json.get('preset_data', None),
                       json.get('type', None),
                       json.get('private', None),
                       json.get('rating', None),
                       json.get('rating_count', None),
                       json.get('user_uri', None),
                       json.get('preview_image_url', None),
                       json.get('created', None),
                       json.get('updated', None))
