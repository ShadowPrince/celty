def check(button, data, validators, translators):
    """
    Check data from button's grab with validators and pass data trough translators.

    button -- button element
    data -- dict of grabbed data
    validators -- dict of validators (name => validator or list of em)
    translators -- dict of translators (name => translator or list of em)

    Returns tuple of cleaned_data and errors dict (name => list of errors).
    """
    errors = {}
    cleaned_data = {}

    if len(data) == 0:
        return None, True

    for k, vs in validators.items():
        value = data.get(k, None)
        for v in (vs if isinstance(vs, list) else [vs]):
            try:
                val_result = v(value)
            except ValueError, e:
                val_result = str(e)
            except TypeError, e:
                val_result = str(e)

            if val_result != None:
                errlist = errors.get(k, [])
                errlist.append(val_result)
                errors[k] = errlist
            else:
                cleaned_value = value
                ts = translators.get(k, [])
                for t in (ts if isinstance(ts, list) else [ts]):
                    cleaned_value = t(cleaned_value)

                cleaned_data[k] = cleaned_value

    return cleaned_data, errors


def errorlines(err):
    """
    Join errors dict into list of strings.
    """
    if not isinstance(err, dict):
        yield ""
    else:
        for k, v in err.items():
            yield "Field {}: ".format(k)
            for e in v:
                yield "  " + str(e)


def errortext(err):
    """
    Join errors dict into string.
    """
    return "\n".join(errorlines(err))


def not_empty():
    """
    Validator. Check if not empty.
    """
    def check(x):
        if not len(x):
            return "should not be empty!"
    return check


def length_in(range):
    """
    Validator. Check if length of value is in python's range iterable.
    """
    def check(x):
        if not len(x) in range:
            return "invalid length!"
    return check


def value_in(range):
    """
    Validator. Check if value is inside python's range iterable.
    """
    def check(x):
        if not x in range:
            return "invalid value!"
    return check


def integer(base=10):
    """
    Validator. Check if value is integer with base = keyword argument "base".
    @TODO: except raising and get error message
    """
    def check(x):
        if type(x) == int:
            return None
        int(x, base)
    return check


def re_match(regex):
    """
    Validator. Check if value matches with regex.
    """
    def check(x):
        if not re.match(regex, x):
            return "not matches regex {}!".format(regex)
    return check


def split(s=" "):
    """
    Translator. Split value with keyword argument "s".
    """
    def tr(x):
        return x.split(s)
    return tr


def to_integer(base=10):
    """
    Translator. Translate value into int with base = keyword argument "base".
    """
    def tr(x):
        if type(x) == int:
            return x
        return int(x, base)
    return tr
