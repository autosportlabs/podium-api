from podium_api.account import make_account_get
from podium_api.events import (
    make_events_get, make_event_create, make_event_get, make_event_delete,
    make_event_update
    )
from podium_api.devices import (
    make_device_get, make_device_create, make_device_update,
    make_device_delete
    )

class PodiumAPI(object):
    
    def __init__(self, token):
        self.token = token
        self.account = PodiumAccountAPI(token)
        self.events = PodiumEventsAPI(token)
        self.devices = PodiumDevicesAPI(token)


class PodiumAccountAPI(object):

    def __init__(self, token):
        self.token = token
        self.events = PodiumEventsAPI(token)

    def get(self, *args, **kwargs):
        '''
        Request that returns the account for the provided authentication token.
        Hits the api/v1/account endpoint with a GET request.

        Kwargs:
            expand (bool): Expand all objects in response output.
            Defaults to False

            quiet (object): If not None HTML layout will not render endpoint
            description. Defaults to None.

            success_callback (function): Callback for a successful request,
            will have the signature:
                on_success(account (PodiumAccount))
            Defaults to None.

            failure_callback (function): Callback for redirects, failures, and
            errors. Will have the signature:
                on_failure(failure_type (string), result (dict), data (dict))
            Values for failure type are: 'error', 'redirect', 'failure'. 
            Defaults to None.

            progress_callback (function): Callback for progress updates,
            will have the signature:
                on_progress(current_size (int), total_size (int), data (dict))
            Defaults to None.

        Return:
            UrlRequest: The request being made.

        '''
        make_account_get(self.token, *args, **kwargs)


class PodiumDevicesAPI(object):
    def __init__(self, token):
        self.token = token

    def create(self, *args, **kwargs):
    '''
    Request that creates a new PodiumDevice.

    The uri for the newly created event will be provided to the
    redirect_callback if one is provided in the form of a PodiumRedirect.

    Args:
        name(str): Name of the device.

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

    '''
        make_device_create(self.token, *args, **kwargs)

    def update(self, *args, **kwargs):
    '''
    Request that updates a PodiumDevice

    Args:
        device_uri (str): URI for the device you are updating.

    Kwargs:
        name(str): Name of the device.

        success_callback (function): Callback for a successful request,
        will have the signature: 
            on_success(result (dict), updated_uri (str))
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

    '''
        make_device_update(self.token, *args, **kwargs)

    def get(self, *args, **kwargs):
    '''
    Request that returns a PodiumDevice for the provided device_uri

    Args:
        device_uri (str): URI for the device you want.

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

    '''
        make_device_get(self.token, *args, **kwargs)

    def delete(self, *args, **kwargs):
    '''
    Deletes the device for the provided URI.

    Args:
        device_uri (str): URI for the device you want.

    Kwargs:
        success_callback (function): Callback for a successful request,
        will have the signature:
            on_success(deleted_uri (str))
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

    '''
        make_device_delete(self.token, *args, **kwargs)



class PodiumEventsAPI(object):

    def __init__(self, token):
        self.token = token

    def list(self, *args, **kwargs):
        '''
        Request that returns a PodiumPagedRequest of events. 
        By default a get request to 
        'https://podium.live/api/v1/events' will be made.

        Kwargs:
            expand (bool): Expand all objects in response output. 
            Defaults to True

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

            start (int): Starting index for events list. 0 indexed.

            per_page (int): Number per page of results, max of 100.

            endpoint (str): If provided the start, per_page, expand, and quiet
            params will not be used instead making a request based on the
            provided endpoint.

        Return:
            UrlRequest: The request being made.

        '''
        make_events_get(self.token, *args, **kwargs)

    def get(self, *args, **kwargs):
        '''
        Request that returns a PodiumEvent for the provided event_uri. 

        Args:
            event_uri (str): URI for the event you want.

        Kwargs:
            expand (bool): Expand all objects in response output.
            Defaults to True

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

        '''
        make_event_get(self.token, *args, **kwargs)

    def delete(self, *args, **kwargs):
        '''
        Deletes the event for the provided URI.

        Args:
            event_uri (str): URI for the event you want.

        Kwargs:
            success_callback (function): Callback for a successful request,
            will have the signature:
                on_success(deleted_uri (str))
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

        '''
        make_event_delete(self.token, *args, **kwargs)

    def create(self, *args, **kwargs):
        '''
        Request that creates a new PodiumEvent.

        The uri for the newly created event will be provided to the
        redirect_callback if one is provided in the form of a PodiumRedirect.

        Args:
            title (str): title for the vent.

            start_time (str): Starting time, use ISO 8601 format.

            end_time (str): Ending time, use ISO 8601 format.

        Kwargs:
            venue_id(str): ID for the venue of event.

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

        '''
        make_event_create(self.token, *args, **kwargs)

    def update(self, *args, **kwargs):
        '''
        Request that updates a PodiumEvent.

        The uri for the newly created event will be provided to the
        redirect_callback if one is provided in the form of a PodiumRedirect.

        Args:
            event_uri (str): URI for the event you are updating.

        Kwargs:
            venue_id(str): ID for the venue of event.

            title (str): title for the vent.

            start_time (str): Starting time, use ISO 8601 format.

            end_time (str): Ending time, use ISO 8601 format.

            success_callback (function): Callback for a successful request,
            will have the signature: 
                on_success(result (dict), updated_uri (str))
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

        '''
        make_event_update(self.token, *args, **kwargs)
