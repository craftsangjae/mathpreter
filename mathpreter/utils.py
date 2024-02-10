def is_numeric(text: str):
    """ whether text is numeric text (both integer and float)

    :param text:
    :return:
    """
    import re
    return bool(re.match(r'([0-9]*[.])?[0-9]+$', text))
