
def is_list_of_elements(instance, element_type):
    return isinstance(instance, list) and all(isinstance(item, element_type) for item in instance)


def is_optional_list_of_elements(instance, element_type):
    return instance is None or is_list_of_elements(instance, element_type)


def is_optional_isinstance(instance, type):
    return instance is None or isinstance(instance, type)


def convert_str_to_enum(enum_type, value):
    if value:
        for member in enum_type:
            if member.value == value:
                return member
    return None
