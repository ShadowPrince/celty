
def check(button, data, validators, translators):
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
    if not isinstance(err, dict):
        yield ""
    else:
        for k, v in err.items():
            yield "Field {}: ".format(k)
            for e in v:
                yield "  " + str(e)


def not_empty():
    def check(x):
        if not len(x):
            return "should not be empty!"
    return check


def length_in(range):
    def check(x):
        if not len(x) in range:
            return "invalid length!"
    return check


def value_in(range):
    def check(x):
        if not x in range:
            return "invalid value!"
    return check


def integer(base=10):
    def check(x):
        int(x, base)
    return check


def re_match(regex):
    def check(x):
        if not re.match(regex, x):
            return "not matches regex {}!".format(regex)
    return check


def split(s=" "):
    def tr(x):
        return x.split(s)
    return tr


def to_integer(base=10):
    def tr(x):
        return int(x, base)
    return tr
