from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.http import HttpResponse

def favicon(request):
    return HttpResponse(status=204)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('items/', include('items.urls')),
    path('auth/', include('users.urls')),
    path('favicon.ico', favicon),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

