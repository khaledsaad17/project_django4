from django.urls import path
from . import views

urlpatterns = [
    path('login',views.login,name="login"),
    path('log_in',views.enter_system,name="enter_system"),
    path('card/',views.card,name="card"),
    path("update_quantity/", views.update_quantity, name="update_quantity"),
    path("remove_product/", views.remove_product, name="remove_product"),
    path("sign_out/", views.sign_out, name="sign_out"),
    path('checkout/', views.checkout, name='checkout'),
    path('process-checkout/', views.process_checkout, name='process_checkout'),
]