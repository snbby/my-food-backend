from django.contrib import admin
from django.urls import include, path
from myfood.api_nin import api


def trigger_error(request):
    division_by_zero = 1 / 0
    print(division_by_zero)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sentry-debug/', trigger_error),
    path('api-nin/', api.urls),
    path('api/', include('myfood.drf_urls')),
]
