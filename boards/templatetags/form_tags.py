from django import template

register = template.Library()


@register.filter
def field_type(bound_field):
    """
    :param bound_field: a django.forms form class field
    :return: A string to showing the django.forms field type
    i.e TextInput for textInput fields, PasswordInput for
    password fields, etc
    """
    return bound_field.field.widget.__class__.__name__


@register.filter
def input_class(bound_field):
    """
    :param bound_field: a django.forms form class field
    :return: a css string for the field
    """
    css_class = ''
    if bound_field.form.is_bound:
        if bound_field.errors:
            css_class = 'is-invalid'
        elif field_type(bound_field) != 'PasswordInput':
            css_class = 'is-valid'
    return 'form-control {}'.format(css_class)
