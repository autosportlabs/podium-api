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

        **mapping_type_id** (int): ID of the mapping type

        **mapping_type** (str): string key representation of the mapping type

        **updated** (str): Date preset was updated. ISO 8601 format.

        **created** (str): Date preset was created. ISO 8601 format.
    """

    def __init__(self, preset_id, uri, name, notes, preset, mapping_type_id, mapping_type, updated, created):
        self.preset_id = preset_id
        self.uri = uri
        self.name = name
        self.notes = notes
        self.preset = preset
        self.mapping_type_id = mapping_type_id
        self.mapping_type = mapping_type
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
                       json.get('preset', None),
                       json.get('mapping_type_id', None),
                       json.get('mapping_type', None),
                       json.get('created', None),
                       json.get('updated', None))
