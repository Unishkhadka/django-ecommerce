from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from ecommerce import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("ecommerce.urls")),
    path('user/', include("users.urls")),
    path('backend/', include("admins.urls")),
]

handler404 = views.error_404
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)