
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django import template

register = template.Library()


# Create your tags here
@register.simple_tag
def get_url(dictionary, key):
    """
    """
    print(dictionary.get(key))

    return dictionary.get(key)




#
