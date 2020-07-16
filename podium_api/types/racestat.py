#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Racestat(object):
    """
    Object that represents a race statistic snapshot

    **Attributes:**
        **racestat_id** (str): Unique id for this racestat

        **comp_number** (str): Competitor number assigned for the race

        **comp_class** (str): Competitor class assigned for the race

        **total_laps** (int): Total number of laps according to timing and scoring

        **last_lap_time** (float): Last lap time according to timing and scoring

        **position_overall** (int): Overall race position

        **position_in_class** (int): Position in class

        **comp_number_ahead** (str): competitor number of competitor ahead
        
        **comp_number_behind** (str): competitor number of competitor behind
        
        **gap_to_ahead** (float): time gap to competitor ahead
        
        **gap_to_behind** (float): time gap to competitor behind
        
        **laps_to_ahead** (int): laps to competitor ahead
        
        **laps_to_behind** (int): laps to competitor behind
        
        **fc_flag** (int): full course flag status
        
        **comp_flag** (int): competitor flag status
        
        **eventdevice_uri:** (str): URI of the eventdevice this racestat belongs to
        
        **device_uri:** (str): URI of the device this racestat belongs to
        
        **user_uri** (str): URI of the user this racestat belongs to        
    """

    def __init__(self, racestat_id, uri, comp_number, comp_class, total_laps, last_lap_time,
                 position_overall, position_in_class, comp_number_ahead, comp_number_behind,
                 gap_to_ahead, gap_to_behind, laps_to_ahead, laps_to_behind,
                 fc_flag, comp_flag,
                 eventdevice_uri, device_uri, user_uri):
        self.racestat_id = racestat_id
        self.uri = uri
        self.comp_number = comp_number
        self.comp_class = comp_class
        self.total_laps = total_laps
        self.last_lap_time = last_lap_time
        self.position_overall = position_overall
        self.position_in_class = position_in_class
        self.comp_number_ahead = comp_number_ahead
        self.comp_number_behind = comp_number_behind
        self.gap_to_ahead = gap_to_ahead
        self.gap_to_behind = gap_to_behind
        self.laps_to_ahead = laps_to_ahead
        self.laps_to_behind = laps_to_behind
        self.fc_flag = fc_flag
        self.comp_flag = comp_flag
        self.eventdevice_uri = eventdevice_uri
        self.device_uri = device_uri
        self.user_uri = user_uri


def get_racestat_from_json(json):
    """
    Returns a Racestat object from the json dict received from podium api.

    Args:
        json (dict): Dict of data from REST api

    Return:
        Racestat: The Racestat object for the data.
    """
    return Racestat(json['id'], json['URI'], json['comp_number'], json['comp_class'],
                         json['total_laps'], json['last_lap_time'],
                         json['position_overall'], json['position_in_class'],
                         json['comp_number_ahead'], json['comp_number_behind'],
                         json['gap_to_ahead'], json['gap_to_behind'],
                         json['laps_to_ahead'], json['laps_to_behind'],
                         json['fc_flag'], json['comp_flag'],
                         json['eventdevice_uri'], json['device_uri'], json['user_uri'])
