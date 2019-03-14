
# urls for each model

method_urls = {
    'list': 'panel:method_list',
    'create': 'panel:method_create',
    'view': 'panel:method_view',
    'delete': 'panel:method_delete',
    'update': 'panel:method_update',
}

zone_urls = {
    'list': 'panel:zone_list',
    'create': 'panel:zone_create',
    'view': 'panel:zone_view',
    'delete': 'panel:zone_delete',
    'update': 'panel:zone_update',
}

shipper_urls = {
    'list': 'panel:shipper_list',
    'create': 'panel:shipper_create',
    'view': 'panel:shipper_view',
    'delete': 'panel:shipper_delete',
    'update': 'panel:shipper_update',
}

constraint_urls = {
    'list': 'panel:constraint_list',
    'create': 'panel:constraint_create',
    'view': 'panel:constraint_view',
    'delete': 'panel:constraint_delete',
    'update': 'panel:constraint_update',
}


# exclude attributes for each model

shipper_create_exclude_fields = ['created_date', 'updated_date', 'shipping_shipper']
shipper_list_exclude_fields = ['created_date', 'shipping_shipper']
shipper_update_exclude_fields = ['created_date', 'updated_date', 'shipping_shipper']
shipper_view_exclude_fields = ['shipping_shipper']

zone_create_exclude_fields = ['created_date', 'updated_date']
zone_list_exclude_fields = ['created_date', 'region', 'province', 'country', 'methods', 'postal_code']
zone_update_exclude_fields = ['created_date', 'updated_date']
zone_view_exclude_fields = []

method_create_exclude_fields = ['created_date', 'updated_date', 'shipping_methods']
method_list_exclude_fields = ['updated_date', 'constraints', 'shipping_methods']
method_update_exclude_fields = ['created_date', 'updated_date', 'shipping_methods']
method_view_exclude_fields = ['shipping_methods']

constraint_create_exclude_fields = ['created_date', 'updated_date', 'shipping_constraints']
constraint_list_exclude_fields = ['created_date', 'shipping_methods', 'shipping_constraints']
constraint_update_exclude_fields = ['created_date', 'updated_date', 'shipping_constraints']
constraint_view_exclude_fields = ['shipping_constraints']


# field types

related_fields = ['ManyToManyField', 'ManyToOneRel']

# redirect urls

shipper_redirect = 'panel:shipper_list'
zone_redirect = 'panel:zone_list'
method_redirect = 'panel:method_list'
constraint_redirect = 'panel:constraint_list'




#
