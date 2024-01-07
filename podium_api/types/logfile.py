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

    def __init__(self, upload_url, file_key, eventdevice_id, status):
        self.upload_url = upload_url
        self.file_key = file_key
        self.eventdevice_id = eventdevice_id
        self.status = status


def get_logfile_from_json(json):
    """
    Returns a PodiumLogfile object from the json dict received from
    podium api.

    Args:
        json (dict): Dict of data from REST api

    Return:
        PodiumFriendship: The PodiumFriendship object for the data.

    """
    return PodiumLogfile(json["upload_url"], json["file_key"], json["eventdevice_id"], json["status"])
