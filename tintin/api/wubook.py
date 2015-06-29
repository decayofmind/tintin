import xmlrpclib

from tintin.errors import ApiError


class WuBookApiError(ApiError):
    def __init__(self, message, code):
        super(WuBookApiError, self).__init__(message, code)


class WuBookApi(object):
    # move it to Base class???
    _methods = [
        "get_token",
        "is_token_valid",
        "release_token",
        "fetch_rooms",
        "new_room",
        "new_virtual_room",
        "mod_room",
        "mod_virtual_room",
        "del_room",
        "room_images",
        "update_rooms_values",
        "update_sparse_rooms_values",
        "fetch_rooms_values",
        "push_update_activation",
        "push_update_url",
        "fetch_bookings",
        "fetch_bookings_codes",
        "fetch_booking",
        "fetch_new_bookings",
        "mark_bookings",
        "push_activation",
        "push_url",
        "cancel_reservation",
        "new_reservation",
        "fetch_otas",
        "bcom_rooms_rates"
        # ... and many more
    ]

    _endpoint = "https://wubook.net/xrws/"

    _server = xmlrpclib.Server(_endpoint)

    def __init__(self):
        def produce_method(method):
            def f(*args):
                return self._request(method, *args)
            return f

        for method in self._methods:
            setattr(self, method, produce_method(method))

    def _request(self, method, *args):
        try:
            result, data = getattr(self._server, method)(*args)
        except ValueError:
            data = getattr(self._server, method)(*args)
            result = 0
        if result != 0:
            raise WuBookApiError(data, result)
        return data