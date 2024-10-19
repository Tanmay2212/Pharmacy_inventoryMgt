from django.contrib import admin
from django.urls import path, include
from inventory.views import home  # Import the home view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # This handles the root URL for the project
    path('inventory/', include('inventory.urls')),  # Ensure this is correct
]
