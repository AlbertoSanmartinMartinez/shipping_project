
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from shipping_app import views as shipping_views
from shipping_app import models as shipping_models


urlpatterns = [

    path('', shipping_views.home, name='home'),

    path('acceso/', shipping_views.custom_login, name='custom_login'),
    path('desconectar/', auth_views.LogoutView.as_view(), name='logout'),


    # shipper urls
    path('transportistas/',
        shipping_views.CustomListView.as_view(
            model=shipping_models.Shipper),
        name='shipper_list'),

    path('transportistas/crear',
        shipping_views.CustomCreateView.as_view(
            model=shipping_models.Shipper),
        name='shipper_create'),

    path('transportistas/<int:id>/editar',
        shipping_views.CustomUpdateView.as_view(
            model=shipping_models.Shipper),
        name='shipper_update'),

    path('transportistas/<int:id>/ver',
        shipping_views.CustomDetailView.as_view(
            model=shipping_models.Shipper),
        name='shipper_view'),

    path('transportistas/<int:id>/borrar',
        shipping_views.CustomDeleteView.as_view(
            model=shipping_models.Shipper),
        name='shipper_delete'),


    # zone urls
    path('zonas/',
        shipping_views.CustomListView.as_view(
            model=shipping_models.Zone),
        name='zone_list'),

    path('zonas/crear',
        shipping_views.CustomCreateView.as_view(
            model=shipping_models.Zone),
        name='zone_create'),

    path('zonas/<int:id>/editar',
        shipping_views.CustomUpdateView.as_view(
            model=shipping_models.Zone),
        name='zone_update'),

    path('zonas/<int:id>/ver',
        shipping_views.CustomDetailView.as_view(
            model=shipping_models.Zone),
        name='zone_view'),

    path('zonas/<int:id>/borrar',
        shipping_views.CustomDeleteView.as_view(
            model=shipping_models.Zone),
        name='zone_delete'),


    # method urls
    path('metodos_envio/',
        shipping_views.CustomListView.as_view(
            model=shipping_models.Method),
        name='method_list'),

    path('metodos_envio/crear',
        shipping_views.CustomCreateView.as_view(
            model=shipping_models.Method),
        name='method_create'),

    path('metodos_envio/<int:id>/editar',
        shipping_views.CustomUpdateView.as_view(
            model=shipping_models.Method),
        name='method_update'),

    path('metodos_envio/<int:id>/ver',
        shipping_views.CustomDetailView.as_view(
            model=shipping_models.Method),
        name='method_view'),

    path('metodos_envio/<int:id>/borrar',
        shipping_views.CustomDeleteView.as_view(
            model=shipping_models.Method),
        name='method_delete'),


    # constraints urls
    path('restricciones/',
        shipping_views.CustomListView.as_view(
            model=shipping_models.Constraint),
        name='constraint_list'),

    path('restricciones/crear',
        shipping_views.CustomCreateView.as_view(
            model=shipping_models.Constraint),
        name='constraint_create'),

    path('restricciones/<int:id>/editar',
        shipping_views.CustomUpdateView.as_view(
            model=shipping_models.Constraint),
        name='constraint_update'),

    path('restricciones/<int:id>/ver',
        shipping_views.CustomDetailView.as_view(
            model=shipping_models.Constraint),
        name='constraint_view'),

    path('restricciones/<int:id>/borrar',
        shipping_views.CustomDeleteView.as_view(
            model=shipping_models.Constraint),
        name='constraint_delete'),
]




#
