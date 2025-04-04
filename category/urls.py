from django.urls import path
from . import views


urlpatterns = [
    path('medication/', views.medication_category, name='medication'),
    path('skincare/', views.skincare_category, name='skincare'),
    path('makeup/', views.makeup_category, name='makeup'),
    path('haircare/', views.haircare_category, name='haircare'),
    path('baby_mom/', views.Baby_Mom_category, name='baby_mom'),
    path('toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorites, name='favorites'),
]
