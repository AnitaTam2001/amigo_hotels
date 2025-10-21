from django.test import TestCase
from .models import Hotel

class HotelModelTests(TestCase):
    def test_hotel_creation(self):
        hotel = Hotel.objects.create(
            name="Amigo Test Hotel",
            location="Test City",
            description="Test description",
            price_per_night=100.00
        )
        self.assertEqual(hotel.name, "Amigo Test Hotel")