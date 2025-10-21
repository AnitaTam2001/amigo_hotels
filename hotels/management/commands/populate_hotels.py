from django.core.management.base import BaseCommand
from hotels.models import Hotel

class Command(BaseCommand):
    help = 'Populate database with sample hotels'

    def handle(self, *args, **options):
        hotels_data = [
            {
                'name': 'Amigo Beach Resort',
                'location': 'Cancun, Mexico',
                'description': 'Beautiful beachfront resort with all-inclusive packages and friendly service.',
                'price_per_night': 199.99,
                'image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80'
            },
            {
                'name': 'Amigo City Hotel',
                'location': 'Mexico City, Mexico',
                'description': 'Modern hotel in the heart of the city with authentic Mexican hospitality.',
                'price_per_night': 129.99,
                'image_url': 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80'
            },
            {
                'name': 'Amigo Mountain Lodge',
                'location': 'Monterrey, Mexico',
                'description': 'Cozy lodge nestled in the mountains with stunning views and warm service.',
                'price_per_night': 149.99,
                'image_url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80'
            },
        ]

        for hotel_data in hotels_data:
            Hotel.objects.create(**hotel_data)
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated Amigo Hotels with sample data!')
        )