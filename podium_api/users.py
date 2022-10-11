#!/usr/bin/env python
# -*- coding: utf-8 -*-
from podium_api.asyncreq import get_json_header_token, make_request_custom_success
from podium_api.types.user import get_user_from_json


def make_user_get(
    token,
    endpoint,
    expand=False,
    quiet=None,
    success_callback=None,
    failure_callback=None,
    progress_callback=None,
    redirect_callback=None,
):
    """
    Returns a PodiumUser object found at the uri provided in the endpoint
    arg.

    Args:
        token (PodiumToken): The authentication token for this session.

        endpoint (str): The URI to make the request to. Typically should be
        provided by some api object.

    Kwargs:
        expand (bool): Expand all objects in response output. Defaults to False

        quiet (object): If not None HTML layout will not render endpoint
        description. Defaults to None.

        success_callback (function): Callback for a successful request,
        will have the signature:
            on_success(token (string))
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
        endpoint,
        users_success_handler,
        method="GET",
        success_callback=success_callback,
        failure_callback=failure_callback,
        progress_callback=progress_callback,
        redirect_callback=redirect_callback,
        params=params,
        header=header,
    )


def make_user_update(
    token,
    user_uri,
    email=None,
    password=None,
    current_password=None,
    time_zone=None,
    username=None,
    name=None,
    avatar_name=None,
    avatar_data=None,
    profile_image_name=None,
    profile_image_data=None,
    description=None,
    permalink=None,
    links=None,
    success_callback=None,
    failure_callback=None,
    progress_callback=None,
    redirect_callback=None,
):
    """
    Request that updates a PodiumUser

    Args:
        token (PodiumToken): The authentication token for this session.

        user_uri (str): URI for the user you are updating.

    Kwargs:
        username(str): Username.

        name(str): Name of the user.

        avatar_name(str): filename of the avatar image.

        avatar_data(str): Base 64 encoded avatar image data.

        profile_image_name(str): filename of the avatar image.

        profile_image_data(str): Base 64 encoded avatar image data.

        description(str): Description of the profile provided by the user.

        permalink(str): Public url for user profile.

        links(list): Links displayed in user profile.

        success_callback (function): Callback for a successful request,
        will have the signature:
            on_success(result (dict), updated_uri (str))

        failure_callback (function): Callback for failures and errors.
        Will have the signature:
            on_failure(failure_type (string), result (dict), data (dict))
        Values for failure type are: 'error', 'failure'.

        redirect_callback (function): Callback for redirect,
        Will have the signature:
            on_redirect(redirect_object (PodiumRedirect))

        progress_callback (function): Callback for progress updates,
        will have the signature:
            on_progress(current_size (int), total_size (int), data (dict))

    Return:
        UrlRequest: The request being made.

    """
    body = {}

    if email:
        body["user[email]"] = email
    if password:
        body["user[password]"] = password
    if current_password:
        body["user[current_password]"] = current_password
    if time_zone:
        body["user[time_zone]"] = time_zone

    if username:
        body["user[username]"] = username
    if name:
        body["user[name]"] = name
    if avatar_name and avatar_data:
        body["user[avatar_name]"] = avatar_name
        body["user[avatar_data]"] = avatar_data
    if profile_image_name and profile_image_data:
        body["user[profile_image_name]"] = profile_image_name
        body["user[profile_image_data]"] = profile_image_data
    if description:
        body["user[description]"] = description
    if permalink:
        body["user[permalink]"] = permalink
    if links:
        body["user[links]"] = links  # failing

    header = get_json_header_token(token)
    return make_request_custom_success(
        user_uri,
        user_update_success_handler,
        method="PUT",
        success_callback=success_callback,
        redirect_callback=redirect_callback,
        failure_callback=failure_callback,
        progress_callback=progress_callback,
        body=body,
        header=header,
        data={"updated_uri": user_uri},
    )


def users_success_handler(req, results, data):
    """
    Creates and returns a  PodiumToken to the success_callback found in data.

    Called automatically by **make_login_request**.

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
        data["success_callback"](get_user_from_json(results["user"]))


def user_update_success_handler(req, results, data):
    """
    Success callback after updating an user. Will return the message from
    the server and the device uri to the success_callback.

    Called automatically by **make_user_update**.

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
        data["success_callback"](results, data["updated_uri"])
