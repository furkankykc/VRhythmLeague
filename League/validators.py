from django.core.exceptions import ValidationError


def max_releations(value,_max_count = 10):

    if value and value.count() > _max_count:
        raise ValidationError('Maximum %s related objects are allowed.' % _max_count )


