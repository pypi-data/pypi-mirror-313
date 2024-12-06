import six


def convert_dict(dictionary):
    """Конвертирует значения из словаря в пригодные для записи в rtf-файл."""
    new_dictionary = {}
    for key, value in dictionary.items():
        # if not isinstance(value, basestring):
        try:
            value = six.text_type(value)
        except Exception:  # pylint:disable=broad-exception-caught
            continue
        res = []
        for v in value:
            u_code = ord(v)
            res.append(f"\\u{str(u_code).rjust(4, '0')}\\'3f")

        new_dictionary[key] = ''.join(res)
    return new_dictionary


def do_replace(text, params):
    """Ищет знаки '#' в тексте rtf-шаблона и подставляет значения из словаря."""
    for key_param, value in params.items():
        if key_param in text:
            text = text.replace(f'#{key_param}#', value)
    return text
