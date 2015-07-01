import unittest

from tintin.api.booking import BookingApi
from credentials_private import BOOKINGCOM


class TestBookingApi(unittest.TestCase):
    def setUp(self):
        self.client = BookingApi(
            username=BOOKINGCOM.get('login'),
            password=BOOKINGCOM.get('password'),
            defaults=BOOKINGCOM.get('defaults')
            )

    def test_get_some_response(self):
        data = list(self.client.getCreditcardTypes(creditcard_ids=1))
        self.assertEqual(len(data), 1)
