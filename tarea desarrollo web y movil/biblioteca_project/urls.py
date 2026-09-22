from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("biblioteca.urls")),
]

if settings.DEBUG:
    # Sirve las imágenes subidas (media/) durante el desarrollo. En un
    # despliegue real esto lo haría un servidor web aparte, no Django.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
