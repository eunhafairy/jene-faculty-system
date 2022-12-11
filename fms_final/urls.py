from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('user/', include('accounts.urls')),
    path('posts/', include('posts.urls')),
    path('subjects/', include('subjects.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
