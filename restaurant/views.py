import logging
from django.shortcuts import render, get_object_or_404
from .models import Booking, Menu
from .forms import BookingForm
from django.core import serializers
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework import viewsets, filters, generics
from .serializers import BookingSerializer, MenuSerializer, UserSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'restaurant/home.html')

def about(request):
    return render(request, 'restaurant/about.html')

def reservations(request):
    date = request.GET.get('date', datetime.today().date())
    bookings = Booking.objects.filter(reservation_date=date)
    if not bookings:
        message = "There are many openings available"
        return render(request, 'restaurant/bookings.html', {"message": message})
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'restaurant/bookings.html', {"bookings": booking_json})

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'restaurant/book.html', context)

def menu(request):
    menu_data = Menu.objects.all().order_by('name')
    return render(request, 'restaurant/menu.html', {"menu": menu_data})

def display_menu_item(request, id=None):
    if id:
        try:
            menu_item = Menu.objects.get(pk=id)
            logger.debug(f"Selected menu_item: {menu_item}")
        except Menu.DoesNotExist:
            logger.debug(f"Menu item with id {id} does not exist.")
            return render(request, 'restaurant/menu_item_not_found.html', status=404)
    else:
        menu_item = ""
    return render(request, 'restaurant/menu_item.html', {"menu_item": menu_item})

@csrf_exempt
def bookings(request):
    if request.method == 'POST':
        data = json.load(request)
        exist = Booking.objects.filter(reservation_date=data['reservation_date']).filter(
            reservation_slot=data['reservation_slot']).exists()
        if not exist:
            booking = Booking(
                first_name=data['first_name'],
                reservation_date=data['reservation_date'],
                reservation_slot=data['reservation_slot'],
            )
            booking.save()
        else:
            return HttpResponse("{'error':1}", content_type='application/json')
    
    date = request.GET.get('date', datetime.today().date())
    bookings = Booking.objects.all().filter(reservation_date=date)
    booking_json = serializers.serialize('json', bookings)
    return HttpResponse(booking_json, content_type='application/json')

def menu_item(request, id):
    item = get_object_or_404(Menu, pk=id)
    return render(request, 'restaurant/menu_item.html', {'menu_item': item})

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'reservation_date']
    ordering_fields = ['reservation_date', 'reservation_slot']
    permission_classes = [IsAuthenticated]

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price']
    permission_classes = [IsAuthenticated]

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
