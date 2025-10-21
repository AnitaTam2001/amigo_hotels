from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Hotel

FAQ_DATA = [
    {
        'question': 'What is your cancellation policy?',
        'answer': 'Free cancellation up to 24 hours before check-in.'
    },
    {
        'question': 'Do you offer airport transportation?',
        'answer': 'Yes, we offer airport transportation at most locations.'
    },
    {
        'question': 'Are pets allowed?',
        'answer': 'Some of our Amigo Hotels are pet-friendly.'
    },
    {
        'question': 'What time is check-in and check-out?',
        'answer': 'Check-in: 3:00 PM, Check-out: 11:00 AM.'
    },
    {
        'question': 'Do you have swimming pools?',
        'answer': 'Most of our Amigo Hotels feature swimming pools.'
    }
]

def home(request):
    hotels = Hotel.objects.all()
    return render(request, 'home.html', {'hotels': hotels})

def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotels/hotel_list.html', {'hotels': hotels})

def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    return render(request, 'hotels/hotel_detail.html', {'hotel': hotel})

def search_hotels(request):
    query = request.GET.get('q', '')
    hotels = Hotel.objects.all()
    
    if query:
        hotels = hotels.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )
    
    return render(request, 'hotels/search_results.html', {
        'hotels': hotels,
        'query': query
    })

def book_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    return render(request, 'hotels/booking.html', {'hotel': hotel})

def booking_success(request, booking_id):
    return render(request, 'hotels/booking_success.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def faq(request):
    return render(request, 'faq.html', {'faqs': FAQ_DATA})