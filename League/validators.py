def max_releations(field_value, value, _max_count=10) -> (bool, str):
    print(value.count(), ' | ', _max_count)
    if value and field_value and field_value.count() + value.count() > _max_count:
        return True, ('Maximum %s related objects are allowed.' % int(_max_count))

    return False, ''
