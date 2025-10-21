from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('hotels/', views.hotel_list, name='hotel_list'),
    path('hotels/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('search/', views.search_hotels, name='search_hotels'),
    path('book/<int:hotel_id>/', views.book_hotel, name='book_hotel'),
    path('booking-success/<int:booking_id>/', views.booking_success, name='booking_success'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
]