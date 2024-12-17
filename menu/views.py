import logging
from django.shortcuts import render, get_object_or_404
from .models import Booking, Menu
from .forms import BookingForm
from django.core import serializers
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'menu/home.html')

def about(request):
    return render(request, 'menu/about.html')

def reservations(request):
    date = request.GET.get('date', datetime.today().date())
    bookings = Booking.objects.filter(reservation_date=date)
    if not bookings:
        message = "There are many openings available"
        return render(request, 'menu/bookings.html', {"message": message})
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'menu/bookings.html', {"bookings": booking_json})

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'menu/book.html', context)

def menu(request):
    menu_data = Menu.objects.all().order_by('name')
    return render(request, 'menu/menu.html', {"menu": menu_data})

def display_menu_item(request, id=None):
    if id:
        try:
            menu_item = Menu.objects.get(pk=id)
            logger.debug(f"Selected menu_item: {menu_item}")
        except Menu.DoesNotExist:
            logger.debug(f"Menu item with id {id} does not exist.")
            return render(request, 'menu/menu_item_not_found.html', status=404)
    else:
        menu_item = ""
    return render(request, 'menu/menu_item.html', {"menu_item": menu_item})

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
    return render(request, 'menu/menu_item.html', {'menu_item': item})
