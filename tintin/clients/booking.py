from tintin.api.booking import BookingApi
from tintin.helpers import list_to_dict, cached_property
from tintin.models import BaseCollection


class BookingClient(BookingApi):
    def __init__(self, *args, **kwargs):
        super(BookingClient, self).__init__(*args, **kwargs)

    @cached_property
    def countries(self):
        return list_to_dict(self.getCountries(), 'countrycode')

    @cached_property
    def hotel_facility_types(self):
        return list_to_dict(self.getHotelFacilityTypes(), 'hotelfacilitytype_id')

    @cached_property
    def room_facility_types(self):
        return list_to_dict(self.getRoomFacilityTypes(), 'roomfacilitytype_id')

    def get_hotels(self, facilities="ids", rooms=False, **kwargs):
        """
        Return complete list of hotels with amenities and rooms and other filled params.
        :param facilities: Fetch hotel facilities (as names, ids or none).
        :param rooms:  Fetch rooms.
        :param hotel_ids:  Limit the result to these hotels.
        :param city_ids:   Limit the results to these cities. (optional)
        :param countrycodes:  Limit the results to these countries. (optional)
        :return: :rtype: List of Hotel objects
        """
        hotels = list_to_dict(self.getHotels(**kwargs), 'hotel_id')

        if facilities:
            hotels_facilities = self.getHotelFacilities(hotel_ids=','.join(hotels.keys()))

            for hotel_facility in hotels_facilities:
                try:
                    if facilities == "names":
                        hotels[hotel_facility.hotel_id].facilities.append(self.hotel_facility_types[hotel_facility.hotelfacilitytype_id].name)
                    elif facilities == "ids":
                        hotels[hotel_facility.hotel_id].facilities.append(int(hotel_facility.hotelfacilitytype_id))
                except AttributeError:
                    if facilities == "names":
                        hotels[hotel_facility.hotel_id].facilities = [self.hotel_facility_types[hotel_facility.hotelfacilitytype_id].name]
                    elif facilities == "ids":
                        hotels[hotel_facility.hotel_id].facilities = [int(hotel_facility.hotelfacilitytype_id)]

        if rooms:
            rooms = self.get_rooms(hotel_ids=','.join(hotels.keys()), facilities=facilities)

            for room in rooms:
                try:
                    hotels[room.hotel_id].rooms.append(room)
                except AttributeError:
                    hotels[room.hotel_id].rooms = BaseCollection(room)

        return BaseCollection(*hotels.values())

    def get_rooms(self, facilities="ids", **kwargs):
        """
        Return complete list of rooms with amenities and other filled params.
        :param facilities: Fetch room facilities (as names, ids or none).
        :param hotel_ids:  Limit the result to these hotels.
        :param city_ids:   Limit the results to these cities. (optional)
        :param countrycodes:  Limit the results to these countries. (optional)
        :return: :rtype: List of Room objects
        """
        rooms = list_to_dict(self.getRooms(**kwargs), 'room_id')

        if facilities:
            rooms_facilities = self.getRoomFacilities(**kwargs)

            for room_facility in rooms_facilities:
                try:
                    if facilities == "names":
                        rooms[room_facility.room_id].facilities.append(self.room_facility_types[room_facility.roomfacilitytype_id].name)
                    elif facilities == "ids":
                        rooms[room_facility.room_id].facilities.append(int(room_facility.roomfacilitytype_id))
                except KeyError:
                    pass
                except AttributeError:
                    if facilities == "names":
                        rooms[room_facility.room_id].facilities = [self.room_facility_types[room_facility.roomfacilitytype_id].name]
                    elif facilities == "ids":
                        rooms[room_facility.room_id].facilities = [int(room_facility.roomfacilitytype_id)]
            to_delete = []
            for room in rooms.itervalues():
                if not hasattr(room, 'facilities'):
                    to_delete.append(room.room_id)
            for room_id in to_delete:
                del rooms[room_id]

        return BaseCollection(*rooms.values())

    def get_hotel_availability(self, hotels, arrival, departure, available_rooms=1, guest_qty=2, **kwargs):
        hotel_availability = self.getHotelAvailability(hotel_ids=','.join([h.hotel_id for h in hotels]),
                                                       arrival_date=arrival.strftime('%Y-%m-%d'),
                                                       departure_date=departure.strftime('%Y-%m-%d'),
                                                       available_rooms=str(available_rooms),
                                                       guest_qty=str(guest_qty),
                                                       **kwargs)
        return BaseCollection(*list(hotel_availability))

    def get_changed_hotels(self, last_change, facilities="ids", rooms=False, **kwargs):
        """
        Return list of hotels changed from last_date.
        :param facilities: Fetch room facilities (as names, ids or none).
        :param rooms:  Fetch rooms.
        :param last_change: Date since changes retrieved from.
        :param city_ids:   Limit the results to these cities. (optional)
        :return: :rtype: List of Hotel objects
        """
        hotels = self.getChangedHotels(last_change=last_change, **kwargs)
        return self.get_hotels(hotel_ids=','.join([hotel.hotel_id for hotel in hotels]), facilities=facilities, rooms=rooms)
