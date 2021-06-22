#!/usr/bin/env python
# -*- coding: utf-8 -*-
from podium_api.asyncreq import make_request_custom_success, get_json_header_token
from podium_api.types.paged_response import get_paged_response_from_json
from podium_api.types.rating import get_rating_from_json
from podium_api.types.redirect import get_redirect_from_json
import podium_api


def make_rating_create(token, rateable_type, rateable_id, rating,
                      report=None, success_callback=None, failure_callback=None,
                      progress_callback=None, redirect_callback=None):
    """
    Request that creates or updates a rating for a rateable object.

    The uri for the newly created rating will be provided to the
    redirect_callback if one is provided in the form of a PodiumRedirect.

    Args:
        token (PodiumToken): The authentication token for this session.

        rateable_type (string): type of rateable object. e.g. preset

        rateable_id (int): ID of the object to rate

        rating (float): Rating value

    Kwargs:
        report (int): non zero if the rateable item is to be reported. rating must also be 0

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
    endpoint = '{}/api/v1/{}/{}/ratings'.format(podium_api.PODIUM_APP.podium_url, rateable_type.lower(), rateable_id)

    body = {'rating[rating]': rating}
    if report is not None:
        body["rating[report]"] = report
    header = get_json_header_token(token)
    return make_request_custom_success(
        endpoint, None, method='POST',
        success_callback=success_callback,
        redirect_callback=create_rating_redirect_handler,
        failure_callback=failure_callback,
        progress_callback=progress_callback,
        body=body, header=header,
        data={'_redirect_callback': redirect_callback}
        )

def create_rating_redirect_handler(req, results, data):
    """
    Handles the success redirect of a **make_rating_create** call.

    Returns a PodiumRedirect with a uri for the newly created rating to the
    _redirect_callback found in data.

    Automatically called by **make_rating_create**, will call the
    redirect_callback passed in to **make_rating_create** if there is on.

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
        data['_redirect_callback'](get_redirect_from_json(results, 'rating'))
