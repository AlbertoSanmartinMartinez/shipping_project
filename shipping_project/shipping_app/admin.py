
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin

from shipping_app import models as shipping_models


admin.site.site_header = 'Shipping Project Django Admin'
admin.autodiscover()

# Register your models here.
admin.site.register(shipping_models.Zone)
admin.site.register(shipping_models.Shipper)
admin.site.register(shipping_models.Constraint)
admin.site.register(shipping_models.Method)

admin.site.register(shipping_models.Region)
admin.site.register(shipping_models.Province)
admin.site.register(shipping_models.Country)
