
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('food/', include('food_tracker.urls')),
    path('', include('food_tracker.urls')),
]
