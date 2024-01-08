#!/usr/bin/env python
# -*- coding: utf-8 -*-
import podium_api
from podium_api.asyncreq import get_json_header_token, make_request_custom_success
from podium_api.types.logfile import get_logfile_from_json
from podium_api.types.paged_response import get_paged_response_from_json
from podium_api.types.redirect import get_redirect_from_json


def make_logfile_new(
    token,
    device_id,
    event_id,
    success_callback=None,
    failure_callback=None,
    progress_callback=None,
    redirect_callback=None,
):
    """
    Request that prepares a logfile upload, returning a presigned URL for uploading the logfile which can be POSTed.

    Args:
        token (PodiumToken): The authentication token for this session.

        endpoint (str): The endpoint to make the request too.

        device_id (int): The ID of the device associated with this logfile

    Kwargs:
        event_id (int): The ID of the event to associate with this logfile.
        Defaults to None. If None, an event will be auto-selected or auto-created as needed

        success_callback (function): Callback for a successful request,
        will have the signature:
            on_success(PodiumPagedResponse)
        Defaults to None.

        failure_callback (function): Callback for failures and errors.
        Will have the signature:
            on_failure(failure_type (string), result (dict), data (dict))
        Values for failure type are: 'error', 'failure'. Defaults to None.

        progress_callback (function): Callback for progress updates,
        will have the signature:
            on_progress(current_size (int), total_size (int), data (dict))
        Defaults to None.

    Return:
        UrlRequest: The request being made.

    """
    endpoint = "{}/api/v1/logfiles/new".format(podium_api.PODIUM_APP.podium_url)
    params = {}
    params["device_id"] = device_id
    if event_id is not None:
        params["event_id"] = event_id

    header = get_json_header_token(token)
    return make_request_custom_success(
        endpoint,
        logfile_success_handler,
        method="GET",
        success_callback=success_callback,
        failure_callback=failure_callback,
        progress_callback=progress_callback,
        redirect_callback=redirect_callback,
        params=params,
        header=header,
    )


def make_logfiles_get(
    token,
    start=None,
    per_page=None,
    expand=True,
    success_callback=None,
    redirect_callback=None,
    failure_callback=None,
    progress_callback=None,
):
    """
    Request that returns a PodiumPagedRequest of Logfiles for the user's account.

    Args:
        token (PodiumToken): The authentication token for this session.

        endpoint (str): the endpoint to make the request to.

    Kwargs:
        expand (bool): Expand all objects in response output. Defaults to True

        success_callback (function): Callback for a successful request,
        will have the signature:
            on_success(PodiumPagedResponse)
        Defaults to None.

        failure_callback (function): Callback for failures and errors.
        Will have the signature:
            on_failure(failure_type (string), result (dict), data (dict))
        Values for failure type are: 'error', 'failure'. Defaults to None.

        redirect_callback (function): Callback for redirect,
        Will have the signature:
            on_redirect(result (dict), data (dict))
        Defaults to None.

        progress_callback (function): Callback for progress updates,
        will have the signature:
            on_progress(current_size (int), total_size (int), data (dict))
        Defaults to None.

        start (int): Starting index for events list. 0 indexed.

        per_page (int): Number per page of results, max of 100.

    Return:
        UrlRequest: The request being made.

    """
    params = {}
    if expand is not None:
        params["expand"] = expand
    if start is not None:
        params["start"] = start
    if per_page is not None:
        per_page = min(per_page, 100)
        params["per_page"] = per_page

    endpoint = "{}/api/v1/logfiles".format(podium_api.PODIUM_APP.podium_url)
    header = get_json_header_token(token)
    return make_request_custom_success(
        endpoint,
        logfiles_success_handler,
        method="GET",
        success_callback=success_callback,
        failure_callback=failure_callback,
        progress_callback=progress_callback,
        redirect_callback=redirect_callback,
        params=params,
        header=header,
    )


def make_logfile_get(
    token,
    logfile_uri,
    expand=True,
    quiet=None,
    success_callback=None,
    redirect_callback=None,
    failure_callback=None,
    progress_callback=None,
):
    """
    Request that returns a PodiumLogfile for the provided logfile_uri

    Args:
        token (PodiumToken): The authentication token for this session.

        logfile_uri (str): URI for the logfile you want.

    Kwargs:
        expand (bool): Expand all objects in response output. Defaults to True

        quiet (object): If not None HTML layout will not render endpoint
        description. Defaults to None.

        success_callback (function): Callback for a successful request,
        will have the signature:
            on_success(PodiumEvent)
        Defaults to None.

        failure_callback (function): Callback for failures and errors.
        Will have the signature:
            on_failure(failure_type (string), result (dict), data (dict))
        Values for failure type are: 'error', 'failure'. Defaults to None.

        redirect_callback (function): Callback for redirect,
        Will have the signature:
            on_redirect(result (dict), data (dict))
        Defaults to None.

        progress_callback (function): Callback for progress updates,
        will have the signature:
            on_progress(current_size (int), total_size (int), data (dict))
        Defaults to None.

    Return:
        UrlRequest: The request being made.

    """
    params = {}
    if expand is not None:
        params["expand"] = expand
    if quiet is not None:
        params["quiet"] = quiet
    header = get_json_header_token(token)
    return make_request_custom_success(
        logfile_uri,
        logfile_success_handler,
        method="GET",
        success_callback=success_callback,
        failure_callback=failure_callback,
        progress_callback=progress_callback,
        redirect_callback=redirect_callback,
        params=params,
        header=header,
    )


def make_logfile_create(
    token,
    file_key,
    eventdevice_id,
    success_callback=None,
    failure_callback=None,
    progress_callback=None,
    redirect_callback=None,
):
    """
    Request that adds a logfile for the user whose token is in use.

    The uri for the newly created event will be provided to the
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

        progress_callback (function): Callback for progress updates,
        will have the signature:
            on_progress(current_size (int), total_size (int), data (dict))
        Defaults to None.

    Return:
        UrlRequest: The request being made.

    """
    endpoint = "{}/api/v1/logfiles".format(podium_api.PODIUM_APP.podium_url)
    body = {"logfile[file_key]": file_key, "logfile[eventdevice_id]": eventdevice_id}
    header = get_json_header_token(token)
    return make_request_custom_success(
        endpoint,
        None,
        method="POST",
        success_callback=success_callback,
        redirect_callback=create_logfile_redirect_handler,
        failure_callback=failure_callback,
        progress_callback=progress_callback,
        body=body,
        header=header,
        data={"_redirect_callback": redirect_callback},
    )


def logfile_success_handler(req, results, data):
    """
    Creates and returns a PodiumLogfile.
    Called automatically by **make_logfile_get**.

    Args:
        req (UrlRequest): Instace of the request that was made.

        results (dict): Dict returned by the request.

        data (dict): Wildcard dict for containing data that needs to be passed
        to the various callbacks of a request. Will contain at least a
        'success_callback' key.

    Return:
        None, this function instead calls a callback.

    """
    if data["success_callback"] is not None:
        data["success_callback"](get_logfile_from_json(results["logfile"]))


def create_logfile_redirect_handler(req, results, data):
    """
    Handles the success redirect of a **make_logfile_create** call.

    Returns a PodiumRedirect with a uri for the newly created logfile to the
    _redirect_callback found in data.

    Automatically called by **make_logfile_create**, will call the
    redirect_callback passed in to **make_logfile_create** if there is one.

    Args:
        req (UrlRequest): Instace of the request that was made.

        results (dict): Dict returned by the request.

        data (dict): Wildcard dict for containing data that needs to be passed
        to the various callbacks of a request. Will contain at least a
        'success_callback' key.

    Return:
        None, this function instead calls a callback.

    """
    if data["_redirect_callback"] is not None:
        data["_redirect_callback"](get_redirect_from_json(results, "logfile"))


def logfiles_success_handler(req, results, data):
    """
    Creates and returns a PodiumPagedResponse with Logfile as the payload
    to the success_callback found in data if there is one.

    Called automatically by **make_logfiles_get**.

    Args:
        req (UrlRequest): Instance of the request that was made.

        results (dict): Dict returned by the request.

        data (dict): Wildcard dict for containing data that needs to be passed
        to the various callbacks of a request. Will contain at least a
        'success_callback' key.

    Return:
        None, this function instead calls a callback.

    """
    if data["success_callback"] is not None:
        data["success_callback"](get_paged_response_from_json(results, "logfiles"))
