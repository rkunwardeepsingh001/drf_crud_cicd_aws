from django.urls import path
from .views import RegisterAPI, LoginAPI
from .views import ItemListCreateAPI, ItemDetailAPI


urlpatterns = [
path('register/', RegisterAPI.as_view(), name='register'),
path('login/', LoginAPI.as_view(), name='login'),
]

urlpatterns += [
    path('items/', ItemListCreateAPI.as_view(), name='items_list_create'),
    path('items/<int:pk>/', ItemDetailAPI.as_view(), name='item_detail'),
]