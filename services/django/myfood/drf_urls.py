from django.urls import path

from . import drf_views as views

urlpatterns = [
    path('foodproducts/search/', views.SearchFoodProducts.as_view()),
    path('foodproducts/search_detailed/', views.SearchDetailedFoodProducts.as_view()),
]
