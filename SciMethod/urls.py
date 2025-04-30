from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('scientificmethod.urls')),  # ← home routes come from your app
    path('mdeditor/', include('mdeditor.urls')),  # if using django-mdeditor
]
