#!/usr/bin/env python
# -*- coding: utf-8 -*-
from podium_api.asyncreq import make_request_custom_success, get_json_header_token
from podium_api.types.racestat import get_racestat_from_json
from podium_api.types.redirect import get_redirect_from_json
import podium_api


def make_racestat_get(token, endpoint, expand=False, quiet=None,
                     success_callback=None,
                     failure_callback=None, progress_callback=None,
                     redirect_callback=None):
    """
     Request that returns a Racestat that represents a specific
    racestat found at the URI. 

    Args:
        token (PodiumToken): The authentication token for this session.

    Kwargs:
        expand (bool): Expand all objects in response output. Defaults to False

        quiet (object): If not None HTML layout will not render endpoint
        description. Defaults to None.

        success_callback (function): Callback for a successful request,
        will have the signature:
            on_success(account (PodiumAccount))
        Defaults to None.

        failure_callback (function): Callback for redirects, failures, and
        errors. Will have the signature:
            on_failure(failure_type (string), result (dict), data (dict))
        Values for failure type are: 'error', 'redirect', 'failure'. Defaults
        to None.

        progress_callback (function): Callback for progress updates,
        will have the signature:
            on_progress(current_size (int), total_size (int), data (dict))
        Defaults to None.

        redirect_callback (function): Callback for redirect, 
        Will have the signature:
            on_redirect(result (dict), data (dict))
        Defaults to None.
        
    Return:
        UrlRequest: The request being made.

    """

    params = {'expand': expand}
    if quiet is not None:
        params['quiet'] = quiet
    header = get_json_header_token(token)
    return make_request_custom_success(endpoint, racestat_success_handler,
                                       method='GET',
                                       success_callback=success_callback,
                                       failure_callback=failure_callback,
                                       progress_callback=progress_callback,
                                       redirect_callback=redirect_callback,
                                       params=params, header=header)


def make_racestats_create(token, event_id, racestats, success_callback=None, failure_callback=None,
                         progress_callback=None, redirect_callback=None):
    """
    add a collection of racestats to the specified event id
    Args:
        token (PodiumToken): The authentication token for this session
        
        event_id: The id of the event to apply racestats        
    """
    endpoint = '{}/api/v1/events/{}/racestats'.format(podium_api.PODIUM_APP.podium_url, event_id)
        
    index = 0
    body = {}
    for racestat in racestats:
        body[f'racestat[{index}][device_id]'] = racestat['device_id']
        body[f'racestat[{index}][comp_number]'] = racestat['comp_number']
        body[f'racestat[{index}][comp_class]'] = racestat['comp_class']
        body[f'racestat[{index}][total_laps]'] = racestat['total_laps']
        body[f'racestat[{index}][last_lap_time]'] = racestat['last_lap_time']
        body[f'racestat[{index}][position_overall]'] = racestat['position_overall']
        body[f'racestat[{index}][position_in_class]'] = racestat['position_in_class']
        body[f'racestat[{index}][comp_number_ahead]'] = racestat['comp_number_ahead']
        body[f'racestat[{index}][comp_number_behind]'] = racestat['comp_number_behind']
        body[f'racestat[{index}][gap_to_ahead]'] = racestat['gap_to_ahead']
        body[f'racestat[{index}][gap_to_behind]'] = racestat['gap_to_behind']
        body[f'racestat[{index}][laps_to_ahead]'] = racestat['laps_to_ahead']
        body[f'racestat[{index}][laps_to_behind]'] = racestat['laps_to_behind']
        body[f'racestat[{index}][fc_flag]'] = racestat['fc_flag']
        body[f'racestat[{index}][comp_flag]'] = racestat['comp_flag']
        index += 1

    header = get_json_header_token(token)
    return make_request_custom_success(
        endpoint, None, method='POST',
        success_callback=success_callback,
        redirect_callback=create_racestat_redirect_handler,
        failure_callback=failure_callback,
        progress_callback=progress_callback,
        body=body, header=header,
        data={'_redirect_callback': redirect_callback}
        )
        
def make_racestat_create(token, event_id, device_id, comp_number, comp_class, total_laps,
                         last_lap_time, position_overall, position_in_class,
                         comp_number_ahead, comp_number_behind, gap_to_ahead,
                         gap_to_behind, laps_to_ahead, laps_to_behind,
                         fc_flag, comp_flag,
                         success_callback=None, failure_callback=None,
                         progress_callback=None, redirect_callback=None):
    """
    add a racestat for the specified event_id / device_id

    The uri for the newly created racestat will be provided to the
    redirect_callback if one is provided in the form of a PodiumRedirect.

    Args:
        token (PodiumToken): The authentication token for this session.

    Kwargs:
        success_callback (function): Callback for a successful request,
        will have the signature: 
            on_success(result (dict), data (dict))
        Defaults to None..

        failure_callback (function): Callback for failures and errors. 
        Will have the signature:
            on_failure(failure_type (string), result (dict), data (dict))
        Values for failure type are: 'error', 'failure'. Defaults to None.

        redirect_callback (function): Callback for redirect, 
        Will have the signature:
            on_redirect(redirect_object (PodiumRedirect))
        Defaults to None.

        progress_callback (function): Callback for progress updates,
        will have the signature:
            on_progress(current_size (int), total_size (int), data (dict))
        Defaults to None.

    Return:
        UrlRequest: The request being made.

    """

    endpoint = '{}/api/v1/events/{}/devices/{}/racestat'.format(podium_api.PODIUM_APP.podium_url, event_id, device_id)
    body = {'racestat[comp_number]': comp_number, 'racestat[comp_class]': comp_class,
            'racestat[total_laps]': total_laps, 'racestat[last_lap_time]': last_lap_time,
            'racestat[position_overall]': position_overall, 'racestat[position_in_class]': position_in_class,
            'racestat[comp_number_ahead]': comp_number_ahead, 'racestat[comp_number_behind]': comp_number_behind,
            'racestat[gap_to_ahead]': gap_to_ahead, 'racestat[gap_to_behind]': gap_to_behind,
            'racestat[laps_to_ahead]': laps_to_ahead, 'racestat[laps_to_behind]': laps_to_behind,
            'racestat[fc_flag]': fc_flag, 'racestat[comp_flag]': comp_flag}
    header = get_json_header_token(token)
    return make_request_custom_success(
        endpoint, None, method='POST',
        success_callback=success_callback,
        redirect_callback=create_racestat_redirect_handler,
        failure_callback=failure_callback,
        progress_callback=progress_callback,
        body=body, header=header,
        data={'_redirect_callback': redirect_callback}
        )


def create_racestat_redirect_handler(req, results, data):
    """
    Handles the success redirect of a **make_racestat_create** call.

    Returns a PodiumRedirect with a uri for the newly created event to the
    _redirect_callback found in data. 

    Automatically called by **make_racestat_create**, will call the
    redirect_callback passed in to **make_racestat_create** if there is one.

    Args:
        req (UrlRequest): Instace of the request that was made.

        results (dict): Dict returned by the request.

        data (dict): Wildcard dict for containing data that needs to be passed
        to the various callbacks of a request. Will contain at least a 
        'success_callback' key.

    Return:
        None, this function instead calls a callback.

    """
    if data['_redirect_callback'] is not None:
        data['_redirect_callback'](get_redirect_from_json(results,
                                                          'racestat'))


def racestat_success_handler(req, results, data):
    """
    Creates and returns a Racestat to the success_callback
    found in data.

    Called automatically by **make_account_request**.

    Args:
        req (UrlRequest): Instace of the request that was made.

        results (dict): Dict returned by the request.

        data (dict): Wildcard dict for containing data that needs to be passed
        to the various callbacks of a request. Will contain at least a 
        'success_callback' key.

    Return:
        None, this function instead calls a callback.

    """
    account = results['racestat']
    if account is not None:
        if data['success_callback'] is not None:
            data['success_callback'](get_racestat_from_json(results['racestat']))
    elif data['failure_callback'] is not None:
            data['failure_callback']('None', results, data)
