from tintin.api.base import BaseApi, BaseCursorDataIterator
from tintin.errors import ApiError


class BookingApiError(ApiError):
    def __init__(self, message, code):
        super(BookingApiError, self).__init__(message, code)


class BookingDataIterator(BaseCursorDataIterator):
    _row_limit = 1000

    def __init__(self, request_func, method, rows=None, **kwargs):
        rows = rows or self._row_limit
        super(BookingDataIterator, self).__init__(request_func, method, rows, **kwargs)


class BookingApi(BaseApi):
    _methods = [
        "getChainTypes",
        "getChains",
        "getChangedHotels",
        "getCities",
        "getCountries",
        "getCreditcardTypes",
        "getCreditcards",
        "getDistrictHotels",
        "getFacilityTypes",
        "getHotelDescriptionPhotos",
        "getHotelDescriptionTranslations",
        "getHotelDescriptionTypes",
        "getHotelFacilities",
        "getHotelFacilityTypes",
        "getHotelLogoPhotos",
        "getHotelPhotos",
        "getHotelTranslations",
        "getHotelTypes",
        "getHotels",
        "getRegions",
        "getRegionHotels",
        "getRoomFacilities",
        "getRoomFacilityTypes",
        "getRoomPhotos",
        "getRoomTranslations",
        "getRooms",
        "getHotelThemes",
        "getHotelAvailability",
        "getBlockAvailability",
        "processBooking",
        "getBookingDetails",
    ]

    _endpoint = 'https://distribution-xml.booking.com/json/' + '{}'

    def __init__(self, *args, **kwargs):
        super(BookingApi, self).__init__(endpoint=self._endpoint, **kwargs)

        def produce_method(method):
            def f(**kwargs):
                return BookingDataIterator(self._request, method, **kwargs)
            return f

        for method in self._methods:
            setattr(self, method, produce_method(method))

    def _request(self, method, debug=False, api_format='json', **kwargs):
        method = 'bookings.{}'.format(method)
        data = self.request(method, debug=debug, api_format=api_format, **kwargs)

        if 'message' and 'code' in data:
            raise BookingApiError(data['message'], data['code'])
        return data
