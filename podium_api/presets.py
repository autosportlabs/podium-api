#!/usr/bin/env python
# -*- coding: utf-8 -*-
from podium_api.asyncreq import make_request_custom_success, get_json_header_token
from podium_api.types.paged_response import get_paged_response_from_json
from podium_api.types.preset import get_preset_from_json
from podium_api.types.redirect import get_redirect_from_json
import podium_api


def make_preset_update(token, preset_uri,
                       name=None,
                       notes=None,
                       preset_data=None,
                       private=None,
                       preview_image_name=None,
                       preview_image_data=None,
                       success_callback=None, failure_callback=None,
                       progress_callback=None, redirect_callback=None):
    """
    Request that updates a PodiumPreset.

    Args:
        token (PodiumToken): The authentication token for this session.

        preset_uri (str): URI for the preset you are updating.



    Kwargs:
        name (str): Name for the preset

        notes (str): Notes for the preset

        preset_data (str): JSON data of the preset

        private(int): 1 if the preset is private to the creating user

        preview_image_name(str): Name of the preview image file

        preview_image_data(str): Base 64 encoded preview image data

        success_callback (function): Callback for a successful request,
        will have the signature:
            on_success(result (dict), updated_uri (str))
        Defaults to None..

        failure_callback (function): Callback for failures and errors.
        Will have the signature:
            on_failure(failure_type (string), result (dict), data (dict))
        Values for failure type are: 'error', 'failure'. Defaults to None.

        progress_callback (function): Callback for progress updates,
        will have the signature:
            on_progress(current_size (int), total_size (int), data (dict))
        Defaults to None.

        redirect_callback (function): Callback for redirect,
        Will have the signature:
            on_redirect(redirect_object (PodiumRedirect))
        Defaults to None.

    Return:
        UrlRequest: The request being made.

    """
    body = {}
    if name is not None:
        body['preset[name]'] = name
    if notes is not None:
        body['preset[notes]'] = notes
    if preset_data is not None:
        body['preset[preset_data]'] = preset_data
    if private is not None:
        body['preset[private]'] = int(private)
    if preview_image_name is not None:
        body['preset[preview_image_name]'] = preview_image_name
    if preview_image_data is not None:
        body['preset[preview_image_data]'] = preview_image_data
    header = get_json_header_token(token)
    return make_request_custom_success(
        preset_uri, preset_update_success_handler,
        method="PUT",
        success_callback=success_callback,
        redirect_callback=redirect_callback,
        failure_callback=failure_callback,
        progress_callback=progress_callback,
        body=body, header=header,
        data={'updated_uri': preset_uri}
        )

def make_preset_create(token, name, notes, preset, type, private, preview_image_name, preview_image_data,
                      success_callback=None, failure_callback=None,
                      progress_callback=None, redirect_callback=None):
    """
    Request that creates a new PodiumPreset.

    The uri for the newly created preset will be provided to the
    redirect_callback if one is provided in the form of a PodiumRedirect.

    Args:
        token (PodiumToken): The authentication token for this session.

        name (str): Name for the preset

        notes (str): Notes for the preset

        preset_data (str): JSON data of the preset

        type (str): Key of the mapping type

        private(int): 1 if the preset is private to the creating user

        preview_image_name(str): Name of the preview image file

        preview_image_data(str): Base 64 encoded preview image data

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

        redirect_callback (function): Callback for redirect,
        Will have the signature:
            on_redirect(redirect_object (PodiumRedirect))
        Defaults to None.

    Return:
        UrlRequest: The request being made.

    """
    endpoint = '{}/api/v1/presets'.format(podium_api.PODIUM_APP.podium_url)
    body = {'preset[name]': name,
            'preset[notes]': notes,
            'preset[preset_data]': preset,
            'preset[type]': type,
            'preset[private]': int(private),
            'preset[preview_image_name]': preview_image_name,
            'preset[preview_image_data]': preview_image_data}
    header = get_json_header_token(token)
    return make_request_custom_success(
        endpoint, None, method='POST',
        success_callback=success_callback,
        redirect_callback=create_preset_redirect_handler,
        failure_callback=failure_callback,
        progress_callback=progress_callback,
        body=body, header=header,
        data={'_redirect_callback': redirect_callback}
        )


def make_preset_delete(token, preset_uri,
                      success_callback=None, redirect_callback=None,
                      failure_callback=None, progress_callback=None):
    """
    Deletes the preset for the provided URI.

    Args:
        token (PodiumToken): The authentication token for this session.

        preset_uri (str): URI for the preset you want to delete.

    Kwargs:
        success_callback (function): Callback for a successful request,
        will have the signature:
            on_success(deleted_uri (str))
        Defaults to None.

        redirect_callback (function): Callback for redirect,
        Will have the signature:
            on_redirect(result (dict), data (dict))
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
    header = get_json_header_token(token)
    return make_request_custom_success(preset_uri, preset_delete_handler,
                                       method='DELETE',
                                       success_callback=success_callback,
                                       failure_callback=failure_callback,
                                       progress_callback=progress_callback,
                                       redirect_callback=redirect_callback,
                                       header=header,
                                       data={'deleted_uri': preset_uri})


def make_preset_get(token, preset_uri, expand=True,
                   quiet=None, success_callback=None,
                   redirect_callback=None,
                   failure_callback=None, progress_callback=None):
    """
    Request that returns a PodiumPreset for the provided preset_uri.

    Args:
        token (PodiumToken): The authentication token for this session.

        preset_uri (str): URI for the preset you want.

    Kwargs:
        expand (bool): Expand all objects in response output. Defaults to True

        quiet (object): If not None HTML layout will not render endpoint
        description. Defaults to None.

        success_callback (function): Callback for a successful request,
        will have the signature:
            on_success(PodiumPreset)
        Defaults to None.

        redirect_callback (function): Callback for redirect,
        Will have the signature:
            on_redirect(result (dict), data (dict))
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
    params = {}
    if expand is not None:
        params['expand'] = expand
    if quiet is not None:
        params['quiet'] = quiet
    header = get_json_header_token(token)
    return make_request_custom_success(preset_uri, preset_success_handler,
                                       method='GET',
                                       success_callback=success_callback,
                                       failure_callback=failure_callback,
                                       progress_callback=progress_callback,
                                       redirect_callback=redirect_callback,
                                       params=params, header=header)


def make_presets_get(token, type, search=None, start=None, per_page=None,
                    endpoint=None, expand=True,
                    quiet=None, success_callback=None,
                    redirect_callback=None,
                    failure_callback=None, progress_callback=None):
    """
    Request that returns a PodiumPagedRequest of presets.
    By default a get request to
    'https://podium.live/api/v1/presets' will be made.

    Args:
        token (PodiumToken): The authentication token for this session.

        type (str): The type key to query.

    Kwargs:
        search (string): search string on name or notes

        expand (bool): Expand all objects in response output. Defaults to True

        quiet (object): If not None HTML layout will not render endpoint
        description. Defaults to None.

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

        start (int): Starting index for preset list. 0 indexed.

        per_page (int): Number per page of results, max of 100.

        endpoint (str): If provided this endpoint will be used instead of
        the default: 'https://podium.live/api/v1/presets'

    Return:
        UrlRequest: The request being made.

    """
    if endpoint is None:
        endpoint = '{}/api/v1/presets'.format(podium_api.PODIUM_APP.podium_url)
    params = {"type": type}
    if search is not None:
        params['search'] = search
    if expand is not None:
        params['expand'] = expand
    if quiet is not None:
        params['quiet'] = quiet
    if start is not None:
        params['start'] = start
    if per_page is not None:
        per_page = min(per_page, 100)
        params['per_page'] = per_page

    header = get_json_header_token(token)
    return make_request_custom_success(endpoint, presets_success_handler,
                                       method='GET',
                                       success_callback=success_callback,
                                       failure_callback=failure_callback,
                                       progress_callback=progress_callback,
                                       redirect_callback=redirect_callback,
                                       params=params, header=header)

def preset_delete_handler(req, results, data):
    """
    Returns the URI for the deleted resource to the user set success_callback

    Called automatically by **make_preset_delete**

    Args:
        req (UrlRequest): Instace of the request that was made.

        results (dict): Dict returned by the request.

        data (dict): Wildcard dict for containing data that needs to be passed
        to the various callbacks of a request. Will contain at least a
        'success_callback' key.

    Return:
        None, this function instead calls a callback.
    """
    if data['success_callback'] is not None:
        data['success_callback'](data['deleted_uri'])


def preset_success_handler(req, results, data):
    """
    Creates and returns a PodiumPreset to the success_callback found in data
    if there is one.

    Called automatically by **make_preset_get**

    Args:
        req (UrlRequest): Instace of the request that was made.

        results (dict): Dict returned by the request.

        data (dict): Wildcard dict for containing data that needs to be passed
        to the various callbacks of a request. Will contain at least a
        'success_callback' key.

    Return:
        None, this function instead calls a callback.
    """
    if data['success_callback'] is not None:
        data['success_callback'](get_preset_from_json(results['preset']))


def presets_success_handler(req, results, data):
    """
    Creates and returns a PodiumPagedResponse with PodiumPreset as the payload
    to the success_callback found in data if there is one.

    Called automatically by **make_presets_get**.

    Args:
        req (UrlRequest): Instace of the request that was made.

        results (dict): Dict returned by the request.

        data (dict): Wildcard dict for containing data that needs to be passed
        to the various callbacks of a request. Will contain at least a
        'success_callback' key.

    Return:
        None, this function instead calls a callback.

    """
    if data['success_callback'] is not None:
        data['success_callback'](get_paged_response_from_json(results,
                                                              'presets'))


def create_preset_redirect_handler(req, results, data):
    """
    Handles the success redirect of a **make_preset_create** call.

    Returns a PodiumRedirect with a uri for the newly created preset to the
    _redirect_callback found in data.

    Automatically called by **make_preset_create**, will call the
    redirect_callback passed in to **make_preset_create** if there is on.

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
        data['_redirect_callback'](get_redirect_from_json(results, 'preset'))


def preset_update_success_handler(req, results, data):
    """
    Success callback after updating a preset. Will return the message from
    the server and the preset uri to the success_callback.

    Called automatically by **make_preset_update**.

    Args:
        req (UrlRequest): Instace of the request that was made.

        results (dict): Dict returned by the request.

        data (dict): Wildcard dict for containing data that needs to be passed
        to the various callbacks of a request. Will contain at least a
        'success_callback' key.

    Return:
        None, this function instead calls a callback.

    """
    if data['success_callback'] is not None:
        data['success_callback'](results, data['updated_uri'])
