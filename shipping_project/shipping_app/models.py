
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import ArrayField


# Shipping Models
class Country(models.Model):
    """
    """

    name = models.CharField(verbose_name=_("Nombre"), max_length=50, unique=True)

    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Países'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        super(Country, self).save(*args, **kwargs)


class Region(models.Model):

    name = models.CharField(verbose_name=_("Nombre"), max_length=50, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Comunidad Autonónoma'
        verbose_name_plural = 'Comunidades Autónomas'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        super(Region, self).save(*args, **kwargs)

class Province(models.Model):

    name = models.CharField(verbose_name=_("Nombre"), max_length=50, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        super(Province, self).save(*args, **kwargs)


class Entity(models.Model):
    """
    """

    STATUS = (("Inactivo", "Inactivo"), ("Activo", "Activo"))
    status = models.CharField(verbose_name=_("Estado"), max_length=20, choices=STATUS, default=1)
    created_date = models.DateTimeField(verbose_name=_("Fecha Creación"), auto_now_add=True)
    updated_date = models.DateTimeField(verbose_name=_("Fecha Actualización"), auto_now=True)

    class Meta:
        abstract = True


class Constraint(Entity):
    """
    """

    name = models.CharField(verbose_name=_("Nombre"), max_length=50)
    TYPE = (("Peso", "Peso"), ("Nº Productos", "Nº Productos")) # dimensions: alto, largo, ancho
    type = models.CharField(verbose_name=_("Tipo de Restricción"), max_length=20, choices=TYPE, default=1)
    min_value = models.DecimalField(_("Valor Mínimo"), max_digits=5, decimal_places=2, default=0)
    max_value = models.DecimalField(_("Valor Máximo"), max_digits=5, decimal_places=2, default=1)

    class Meta:
        verbose_name = 'Restricción'
        verbose_name_plural = 'Restricciones'

    def __unicode__(self):
        return self.type + ": mínimo " + str(self.min_value) + " , máximo " + str(self.max_value)

    def __str__(self):
        return self.type + ": mínimo " + str(self.min_value) + " , máximo " + str(self.max_value)


class Shipper(Entity):
    """
    """

    name = models.CharField(verbose_name=_("Nombre"), max_length=50, unique=True)

    class Meta:
        verbose_name = 'Transportista'
        verbose_name_plural = 'Transportistas'

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        super(Shipper, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Method(Entity):
    """
    """

    #TYPE = (("Gratuito", "Gratuito"), ("Precio Fijo", "Precio Fijo"), ("Standard", "Standard"), ("Recogida Local", "Recogida Local"))
    name = models.CharField(verbose_name=_("Nombre"), max_length=50)
    #type = models.CharField(verbose_name=_("Tipo de Envío"), max_length=20, choices=TYPE, default=1)
    shipper = models.ForeignKey(Shipper, verbose_name=_("Transportista"), related_name='shipping_shipper', on_delete=models.SET_NULL, null=True, blank=True)
    constraints = models.ManyToManyField(Constraint, verbose_name=_("Restricciones"), related_name='shipping_constraints', blank=True)
    price = models.DecimalField(_("Precio"), max_digits=8, decimal_places=2)
    duration = models.PositiveIntegerField(verbose_name=_('Tiempo de Entrega'), default=0, blank=True)

    class Meta:
        verbose_name = 'Método de Envío'
        verbose_name_plural = 'Métodos de Envío'

    def __unicode__(self):
        return self.name + str(self.shipper) + " " + str(self.price) + " € " + str(self.duration) + " h"

    def __str__(self):
        return self.name + str(self.shipper) + " " + str(self.price) + " € " + str(self.duration) + " h"


class Zone(Entity):
    """
    """

    name = models.CharField(verbose_name=_("Nombre"), max_length=50)
    country = models.ManyToManyField(Country, verbose_name=_("País"), related_name='country_zone')#, on_delete=models.CASCADE)
    region = models.ManyToManyField(Region, verbose_name=_("Comunidad Autónoma"), related_name='region_zone', blank=True)
    province = models.ManyToManyField(Province, verbose_name=_("Provincia"), related_name='province_zone', blank=True)
    postal_code = models.TextField(verbose_name=_("Código Postal"), null=True, blank=True)
    #postal_code = ArrayField(models.TextField(), verbose_name=_("Código Postal"), null=True, blank=True)
    methods = models.ManyToManyField(Method, verbose_name=_("Métodos de Envio"), related_name='shipping_methods', blank=True)

    class Meta:
        verbose_name = 'Zona'
        verbose_name_plural = 'Zonas'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name




#
