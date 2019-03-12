
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import HttpResponse

from global_login_required import login_not_required

from shipping_app import config as shipping_config
from shipping_app import forms as shipping_forms
from shipping_app import models as shipping_models


# Create your views here.
@login_not_required
def home(request):
    """
    """

    return render(request, 'home.html', {})


@login_not_required
def custom_login(request):
    """
    """

    title = 'Acceso'
    if request.method == 'POST':
        form = shipping_forms.LoginForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)

                    return redirect('panel:shipper_list')

    else:
        form = shipping_forms.LoginForm()

    return render(request, 'login.html', {
        'title': title,
        'form': form,
    })


@login_not_required
def checkout(request):
    """
    """

    methods = shipping_models.Method.objects.all()

    if request.method == 'POST':
        form = shipping_forms.CheckoutForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data

            shippers = shipping_models.Shipper.objects.filter(status='Activo').distinct()
            print(shippers)

            constraints = shipping_models.Constraint.objects.filter(
                Q(status='Activo') &
                ((Q(type='Nº Productos') & Q(min_value__lte=data['num_products']) & Q(max_value__gte=data['num_products'])) | #peso
                (Q(type='Peso') & Q(min_value__lte=data['weight']) & Q(max_value__gte=data['weight']))) # num_products
            ).distinct()
            print(constraints)

            zones = shipping_models.Zone.objects.filter(
                Q(status='Activo') &
                Q(country__name=data['country']) &
                (Q(region__name=data['region']) |
                Q(province__name=data['province']) |
                Q(postal_code__icontains=data['postal_code']))
            ).distinct()
            print(zones)

            methods = methods.filter(
                Q(status='Activo') &
                Q(constraints__in=constraints) &
                Q(shipper__in=shippers) &
                Q(shipping_methods__in=zones)
            ).distinct()
            print(methods)

    else:
        form = shipping_forms.CheckoutForm()

    methods =  methods.order_by('price')[:5]

    return render(request, 'checkout.html', {
        'form': form,
        'methods': methods
    })


class CustomListView(View):
    """
    custom generic list view for all models
    order by attributes
    paginate the content
    show concrete attributes by model
    """

    elements = None
    model = None
    urls = None

    def get(self, request, *args, **kwargs):
        """
        """

        title = self.model._meta.verbose_name_plural

        self.urls = getUrls(self.model._meta.verbose_name_plural)

        if self.elements is None:
            elements = self.model.objects.all().order_by('-created_date')
        else:
            elements = self.elements

        order = request.GET.get('order')
        if order is not None:
            elements = elements.order_by(order)
        else:
            order = '-created_date'

        fields = []
        model_fields = self.model._meta.get_fields()
        exclude_fields = getExcludeFields(self.model._meta.verbose_name_plural, 'list')
        [fields.append(field) for field in model_fields if field.name not in exclude_fields]
        print(fields)

        for element in elements:
            list = []
            for field in fields:
                list.append(getattr(element, field.name))
            element.fields_values = list

        paginator = Paginator(elements, 10)
        page = request.GET.get('page')

        if page is None:
            page = 1

        try:
            elements = paginator.page(page)
        except PageNotAnInteger:
            elements = paginator.page(1)
        except EmptyPage:
            elements = paginator.page(paginator.num_pages)

        return render(request, 'list.html', {
            'elements': elements,
            'fields': fields,
            'urls': self.urls,
            'title': title,
            'order': order,
            'page': page,
        })


class CustomCreateView(View):
    """
    custom generic create view for all models
    generic crete form depends the model
    """

    model = None
    urls = None

    def post(self, request, *args, **kwargs):
        """
        """

        fields = []
        model_fields = self.model._meta.get_fields()
        exclude_fields = getExcludeFields(self.model._meta.verbose_name_plural, 'create')
        [fields.append(field) for field in model_fields if field.name not in exclude_fields]

        form = shipping_forms.get_custom_form(self.model, fields)
        form = form(request.POST)

        if form.is_valid():
            form.save()

            return redirect(getRedirectUrl(self.model._meta.verbose_name_plural))

        else:
            print("formulario invalido")

        return render(request, 'create.html', {
            'form': form,
            'urls': self.urls,
        })

    def get(self, request, *args, **kwargs):
        """
        """

        fields = []
        model_fields = self.model._meta.get_fields()
        exclude_fields = getExcludeFields(self.model._meta.verbose_name_plural, 'create')
        [fields.append(field) for field in model_fields if field.name not in exclude_fields]

        form = shipping_forms.get_custom_form(self.model, fields)

        title = "Crear "
        title += self.model._meta.verbose_name

        self.urls = getUrls(self.model._meta.verbose_name_plural)

        return render(request, 'create.html', {
            'title': title,
            'form': form,
            'urls': self.urls,
        })


class CustomUpdateView(View):
    """
    """

    model = None
    urls = None
    element = None

    def post(self, request, id=None, *args, **kwargs):
        """
        """

        self.urls = getUrls(self.model._meta.verbose_name_plural)

        self.element = get_object_or_404(self.model, id=id)

        fields = []
        model_fields = self.model._meta.get_fields()
        exclude_fields = getExcludeFields(self.model._meta.verbose_name_plural, 'update')
        [fields.append(field) for field in model_fields if field.name not in exclude_fields]

        form = shipping_forms.get_custom_form(self.model, fields)
        form = form(request.POST, instance=self.element)

        if form.is_valid():
            form.save()

            return redirect(getRedirectUrl(self.model._meta.verbose_name_plural))

        else:
            print("formulario invalido")

        return render(request, 'update.html', {
            'form': form,
            'urls': self.urls,
            'element': self.element
        })

    def get(self, request, id=None, *args, **kwargs):
        """
        """

        self.urls = getUrls(self.model._meta.verbose_name_plural)

        self.element = get_object_or_404(self.model, id=id)

        fields = []
        model_fields = self.model._meta.get_fields()
        exclude_fields = getExcludeFields(self.model._meta.verbose_name_plural, 'update')
        [fields.append(field) for field in model_fields if field.name not in exclude_fields]

        form = shipping_forms.get_custom_form(self.model, fields)
        form = form(instance=self.element)

        title = "Editar "
        title += self.model._meta.verbose_name

        self.urls = getUrls(self.model._meta.verbose_name_plural)

        return render(request, 'update.html', {
            'title': title,
            'form': form,
            'urls': self.urls,
            'element': self.element
        })


class CustomDetailView(View):
    """
    """

    element = None
    model = None
    urls = None

    def get(self, request, id=None, *args, **kwargs):
        """
        """

        title = "Ver "
        title += self.model._meta.verbose_name

        self.element = get_object_or_404(self.model, id=id)

        fields = []
        model_fields = self.model._meta.get_fields()
        exclude_fields = getExcludeFields(self.model._meta.verbose_name_plural, 'view')
        [fields.append(field) for field in model_fields if field.name not in exclude_fields]
        print(fields)

        list = {}
        for field in fields:
            if field.__class__.__name__ in shipping_config.related_fields:
                values = []
                for value in getattr(self.element, field.name).all():
                    values.append(str(value))
                list[field.verbose_name] = values
            else:
                list[field.verbose_name] = getattr(self.element, field.name)
        self.element.fields_values = list

        return render(request, 'view.html', {
        'title': title,
        'element': self.element,
    })


class CustomDeleteView(View):
    """
    """

    model = None
    urls = None
    element = None

    def post(self, request, id=None, *args, **kwargs):
        """
        """

        self.urls = getUrls(self.model._meta.verbose_name_plural)

        self.element = get_object_or_404(self.model, id=id)

        title = "Borrar "
        title += self.model._meta.verbose_name

        form = shipping_forms.ConfirmationForm(request.POST)

        if form.is_valid():
            self.element.delete()

            return redirect(getRedirectUrl(self.model._meta.verbose_name_plural))

        else:
            print("formulario invalido")

        return render(request, 'delete.html', {
            'title': title,
            'form': form,
            'urls': self.urls,
            'element': self.element
        })

    def get(self, request, id=None, *args, **kwargs):
        """
        """

        title = "Borrar "
        title += self.model._meta.verbose_name

        self.urls = getUrls(self.model._meta.verbose_name_plural)

        self.element = get_object_or_404(self.model, id=id)

        form = shipping_forms.ConfirmationForm()

        return render(request, 'delete.html', {
        'title': title,
        'element': self.element,
        'form': form,
        'urls': self.urls
    })


def getUrls(name):

    urls = None

    if name == 'Transportistas':
        urls = shipping_config.shipper_urls

    elif name == 'Zonas':
        urls = shipping_config.zone_urls

    elif name == 'Métodos de Envío':
        urls = shipping_config.method_urls

    elif name == 'Restricciones':
        urls = shipping_config.constraint_urls

    return urls


def getRedirectUrl(name):
    """
    """
    print(name)

    url = None

    if name == 'Transportistas':
        url = shipping_config.shipper_redirect

    elif name == 'Zonas':
        url = shipping_config.zone_redirect

    elif name == 'Métodos de Envío':
        url = shipping_config.method_redirect

    elif name == 'Restricciones':
        url = shipping_config.constraint_redirect

    print(url)

    return url


def getExcludeFields(model, action):
    """
    """

    fields = None

    if model == 'Transportistas':
        if action == 'list':
            fields = shipping_config.shipper_list_exclude_fields
        elif action == 'create':
            fields = shipping_config.shipper_create_exclude_fields
        elif action == 'update':
            fields = shipping_config.shipper_update_exclude_fields
        elif action == 'view':
            fields = shipping_config.shipper_view_exclude_fields

    elif model == 'Zonas':
        if action == 'list':
            fields = shipping_config.zone_list_exclude_fields
        elif action == 'create':
            fields = shipping_config.zone_create_exclude_fields
        elif action == 'update':
            fields = shipping_config.zone_update_exclude_fields
        elif action == 'view':
            fields = shipping_config.zone_view_exclude_fields

    elif model == 'Métodos de Envío':
        if action == 'list':
            fields = shipping_config.method_list_exclude_fields
        elif action == 'create':
            fields = shipping_config.method_create_exclude_fields
        elif action == 'update':
            fields = shipping_config.method_update_exclude_fields
        elif action == 'view':
            fields = shipping_config.method_view_exclude_fields

    elif model == 'Restricciones':
        if action == 'list':
            fields = shipping_config.constraint_list_exclude_fields
        elif action == 'create':
            fields = shipping_config.constraint_create_exclude_fields
        elif action == 'update':
            fields = shipping_config.constraint_update_exclude_fields
        elif action == 'view':
            fields = shipping_config.constraint_view_exclude_fields

    return fields


@login_not_required
def checkout_load(request):
    """
    """

    print("load elements function")

    region = request.GET.get('region')
    print(region)

    provinces = shipping_models.Province.objects.filter(region_id=region)
    print(provinces)

    data = serializers.serialize('json', provinces, fields=('id', 'name'))

    return HttpResponse(data, content_type='application/json')




#
