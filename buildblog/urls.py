from django.views.generic import TemplateView
from core import urls as core_urls
from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from blog.views import  TechStackListView
from core.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('', include('blog.urls')),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
