#!/usr/bin/env python
# -*- coding: utf-8 -*-
class PodiumEventDevice(object):
    """
    Object that represents a device at an event.

    **Attributes:**
        **eventdevice_id** (str): Unique id for device at this event

        **uri** (str): URI for this device at this event.

        **channels** (list): List of channels of data. Can be sensors or
        other sources of data.

        **name** (str): Name of device at event. Not always the same as the
        device name.

        **device_uri** (str): URI of the device

        **laps_uri** (str): URI of lap data.

    """

    def __init__(self, eventdevice_id, uri, channels, name, device_uri,
                 laps_uri):
        self.eventdevice_id = eventdevice_id
        self.uri = uri
        self.channels = channels
        self.name = name
        self.device_uri = device_uri
        self.laps_uri = laps_uri
        

def get_eventdevice_from_json(json):
    """
    Returns a PodiumEventDevice object from the json dict received from
    podium api.

    Args:
        json (dict): Dict of data from REST api

    Return:
        PodiumEvent: The PodiumEvent object for this data.
    """
    return PodiumEventDevice(json['id'], json['URI'],
                             json.get('channels', []),
                             json.get('name', None),
                             json.get('device_uri', None),
                             json.get('laps_uri', None))
