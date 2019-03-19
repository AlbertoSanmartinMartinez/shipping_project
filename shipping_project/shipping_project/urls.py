
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from shipping_app import urls as panel_urls
from shipping_app import views as shipping_views

from shipping_project import settings


urlpatterns = [

    # admin urls
    path('admin/', admin.site.urls),

    # panel urls
    path('panel/', include((panel_urls, 'panel'), namespace='panel')),

    # web urls
    path('checkout/', shipping_views.checkout, name='checkout'),
    path('checkout/cargar_elementos/', shipping_views.checkout_load, name='checkout_ajax_load'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
