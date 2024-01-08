#!/usr/bin/env python
# -*- coding: utf-8 -*-
class PodiumLogfile(object):
    """
    Object that represents a Logfile

    **Attributes:**

        **upload_url** (string): URL used to upload the actual logfile

        **file_key** (string): key of logfile, used later to start the import process after the log file is uploaded using the URL

        **eventdevice_id** (id): The ID of the eventdevice associated with this upload

        **status** (int): The state of this logfile, where
          STATUS_UNQUEUED= -1
          STATUS_ERROR = 0
          STATUS_QUEUED = 1
          STATUS_PROCESSING = 2
          STATUS_COMPLETED = 3
    """

    def __init__(
        self,
        file_key,
        eventdevice_id,
        status,
        id=None,
        URI=None,
        upload_url=None,
        event_id=None,
        event_url=None,
        event_title=None,
        device_id=None,
        device_url=None,
        device_name=None,
        created=None,
    ):
        self.file_key = file_key
        self.eventdevice_id = eventdevice_id
        self.status = status

        self.id = id
        self.URI = URI
        self.upload_url = upload_url

        self.event_id = event_id
        self.event_url = event_url
        self.event_title = event_title
        self.device_id = device_id
        self.device_url = device_url
        self.device_name = device_name
        self.created = created


def get_logfile_from_json(json):
    """
    Returns a PodiumLogfile object from the json dict received from
    podium api.

    Args:
        json (dict): Dict of data from REST api

    Return:
        PodiumFriendship: The PodiumFriendship object for the data.

    """
    return PodiumLogfile(
        json["file_key"],
        json["eventdevice_id"],
        json["status"],
        json.get("id", None),
        json.get("URI", None),
        json.get("upload_url", None),
        json.get("event_id", None),
        json.get("event_url", None),
        json.get("event_title", None),
        json.get("device_id", None),
        json.get("device_url", None),
        json.get("device_name", None),
        json.get("created", None),
    )
