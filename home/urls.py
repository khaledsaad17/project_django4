from django.urls import path
from . import views


urlpatterns = [
    path('',views.test,name="home"),
    path('about',views.about,name="about"),
    path('services',views.services,name="services"),
    path('Contact',views.contact_us,name="contact_us"),
    path("add-to-cart/", views.add_to_cart, name="add_to_cart"),
]