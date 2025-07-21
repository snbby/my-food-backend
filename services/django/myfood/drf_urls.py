from django.urls import path

from myfood import drf_views as views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('foodproducts/search/', views.SearchFoodProducts.as_view()),
    path('foodproducts/search_detailed/', views.SearchDetailedFoodProducts.as_view()),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # ReDoc UI (optional)
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
