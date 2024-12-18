from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    path('reservations/', views.reservations, name="reservations"),
    path('menu/', views.menu, name="menu"),
    path('menu_item/<int:id>/', views.display_menu_item, name="menu_item"),  
    path('bookings', views.bookings, name='bookings'), 
    path('api/registration/', views.UserRegistrationView.as_view(), name='registration'),  # Add this line for user registration
]

router = DefaultRouter()
router.register(r'api/bookings', views.BookingViewSet)
router.register(r'api/menu', views.MenuViewSet)

urlpatterns += router.urls
