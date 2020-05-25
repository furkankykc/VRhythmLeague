def max_releations(field_value, value, _max_count=10) -> (bool, str):
    print(len(
        set(field_value.values_list('key', flat=True)) | set(value.values_list('key', flat=True))),
          ' | ', _max_count)
    # todo burada bi sikinti var max rel ile ilgili
    if value and field_value and len(
            set(field_value.values_list('key', flat=True)) | set(value.values_list('key', flat=True))) > _max_count:
        return True, ('Maximum %s related objects are allowed.' % int(_max_count))

    return False, ''
