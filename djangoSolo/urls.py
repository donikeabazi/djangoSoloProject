from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('flowers.urls')),
    path('admin/', admin.site.urls),
]

