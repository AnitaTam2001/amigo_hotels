from django.test import TestCase
from django.urls import reverse
from .models import Hotel, Booking
from datetime import date, timedelta

class HotelModelTests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.hotel = Hotel.objects.create(
            name="Amigo Test Hotel",
            location="Test City, Mexico",
            description="A test hotel for unit testing",
            price_per_night=150.00,
            image_url="https://example.com/test.jpg"
        )
    
    def test_hotel_creation(self):
        """Test that a hotel can be created"""
        self.assertEqual(self.hotel.name, "Amigo Test Hotel")
        self.assertEqual(self.hotel.location, "Test City, Mexico")
        self.assertEqual(self.hotel.price_per_night, 150.00)
        self.assertTrue(isinstance(self.hotel, Hotel))
    
    def test_hotel_string_representation(self):
        """Test the string representation of Hotel model"""
        self.assertEqual(str(self.hotel), "Amigo Test Hotel")
    
    def test_hotel_fields(self):
        """Test that all hotel fields are properly set"""
        self.assertEqual(self.hotel.description, "A test hotel for unit testing")
        self.assertEqual(self.hotel.image_url, "https://example.com/test.jpg")

class BookingModelTests(TestCase):
    def setUp(self):
        """Set up test data for bookings"""
        self.hotel = Hotel.objects.create(
            name="Amigo Beach Resort",
            location="Cancun, Mexico",
            description="Beautiful beach resort",
            price_per_night=199.99
        )
        
        self.booking = Booking.objects.create(
            hotel=self.hotel,
            check_in=date.today() + timedelta(days=7),
            check_out=date.today() + timedelta(days=14),
            guests=2,
            customer_name="John Doe",
            customer_email="john@example.com",
            total_price=1399.93  # 7 nights * 199.99
        )
    
    def test_booking_creation(self):
        """Test that a booking can be created"""
        self.assertEqual(self.booking.customer_name, "John Doe")
        self.assertEqual(self.booking.customer_email, "john@example.com")
        self.assertEqual(self.booking.guests, 2)
        self.assertEqual(self.booking.total_price, 1399.93)
        self.assertTrue(isinstance(self.booking, Booking))
    
    def test_booking_string_representation(self):
        """Test the string representation of Booking model"""
        expected_string = "John Doe - Amigo Beach Resort"
        self.assertEqual(str(self.booking), expected_string)
    
    def test_booking_relationship(self):
        """Test the foreign key relationship between Booking and Hotel"""
        self.assertEqual(self.booking.hotel, self.hotel)
        self.assertEqual(self.booking.hotel.name, "Amigo Beach Resort")

class ViewTests(TestCase):
    def setUp(self):
        """Set up test data for views"""
        self.hotel1 = Hotel.objects.create(
            name="Amigo City Hotel",
            location="Mexico City",
            description="City center hotel",
            price_per_night=129.99
        )
        
        self.hotel2 = Hotel.objects.create(
            name="Amigo Mountain Lodge",
            location="Monterrey",
            description="Mountain retreat",
            price_per_night=149.99
        )
    
    def test_home_view_status_code(self):
        """Test that home page returns 200 status code"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_home_view_template(self):
        """Test that home page uses correct template"""
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')
    
    def test_home_view_context(self):
        """Test that home page context contains hotels"""
        response = self.client.get(reverse('home'))
        self.assertEqual(len(response.context['hotels']), 2)
        self.assertIn(self.hotel1, response.context['hotels'])
        self.assertIn(self.hotel2, response.context['hotels'])
    
    def test_hotel_list_view(self):
        """Test hotel list view"""
        response = self.client.get(reverse('hotel_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hotels/hotel_list.html')
        self.assertEqual(len(response.context['hotels']), 2)
    
    def test_hotel_detail_view(self):
        """Test hotel detail view"""
        response = self.client.get(reverse('hotel_detail', args=[self.hotel1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hotels/hotel_detail.html')
        self.assertEqual(response.context['hotel'], self.hotel1)
    
    def test_hotel_detail_view_404(self):
        """Test that non-existent hotel returns 404"""
        response = self.client.get(reverse('hotel_detail', args=[999]))
        self.assertEqual(response.status_code, 404)
    
    def test_about_view(self):
        """Test about page"""
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')
    
    def test_contact_view(self):
        """Test contact page"""
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')

class SearchTests(TestCase):
    def setUp(self):
        """Set up test data for search"""
        self.beach_hotel = Hotel.objects.create(
            name="Amigo Beach Resort",
            location="Cancun",
            description="Beautiful beachfront property with ocean views",
            price_per_night=199.99
        )
        
        self.city_hotel = Hotel.objects.create(
            name="Amigo City Hotel",
            location="Mexico City",
            description="Modern hotel in downtown area",
            price_per_night=129.99
        )
    
    def test_search_by_name(self):
        """Test searching hotels by name"""
        response = self.client.get(reverse('search_hotels') + '?q=Beach')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['hotels']), 1)
        self.assertEqual(response.context['hotels'][0], self.beach_hotel)
    
    def test_search_by_location(self):
        """Test searching hotels by location"""
        response = self.client.get(reverse('search_hotels') + '?q=Cancun')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['hotels']), 1)
        self.assertEqual(response.context['hotels'][0], self.beach_hotel)
    
    def test_search_by_description(self):
        """Test searching hotels by description"""
        response = self.client.get(reverse('search_hotels') + '?q=modern')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['hotels']), 1)
        self.assertEqual(response.context['hotels'][0], self.city_hotel)
    
    def test_empty_search(self):
        """Test search with empty query returns all hotels"""
        response = self.client.get(reverse('search_hotels') + '?q=')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['hotels']), 2)
    
    def test_no_results_search(self):
        """Test search with no matching results"""
        response = self.client.get(reverse('search_hotels') + '?q=NonExistent')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['hotels']), 0)

class URLTests(TestCase):
    def test_urls(self):
        """Test that all URLs are accessible"""
        urls = [
            reverse('home'),
            reverse('hotel_list'),
            reverse('about'),
            reverse('contact'),
            reverse('search_hotels'),
        ]
        
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
    
    def test_hotel_detail_url(self):
        """Test hotel detail URL pattern"""
        hotel = Hotel.objects.create(
            name="Test Hotel",
            location="Test",
            description="Test",
            price_per_night=100.00
        )
        response = self.client.get(reverse('hotel_detail', args=[hotel.id]))
        self.assertEqual(response.status_code, 200)

class ModelValidationTests(TestCase):
    def test_hotel_price_validation(self):
        """Test that hotel price must be positive"""
        with self.assertRaises(Exception):
            Hotel.objects.create(
                name="Invalid Hotel",
                location="Test",
                description="Test",
                price_per_night=-100.00  # Invalid negative price
            )
    
    def test_booking_guest_validation(self):
        """Test that booking guests must be positive"""
        hotel = Hotel.objects.create(
            name="Test Hotel",
            location="Test",
            description="Test",
            price_per_night=100.00
        )
        
        with self.assertRaises(Exception):
            Booking.objects.create(
                hotel=hotel,
                check_in=date.today(),
                check_out=date.today() + timedelta(days=1),
                guests=0,  # Invalid guest count
                customer_name="Test",
                customer_email="test@example.com",
                total_price=100.00
            )

# Run the tests with: python manage.py test hotels