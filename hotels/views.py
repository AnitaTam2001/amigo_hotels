from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Hotel

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

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')