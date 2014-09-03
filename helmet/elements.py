

def label(*lines, **kwargs):
    """
        max_lines: integer (client-side),
    """
    kwargs.update({
        "type": "label",
        "text": "\n".join(lines), })
    return kwargs


def input(name, value=None):
    return {"type": "input",
            "name": name,
            "value": "" if not value else value, }


def button(caption, command, grab=(), name=None):
    return {"type": "button",
            "name": name,
            "caption": caption,
            "command": command,
            "grab": grab, }


def progressbar(name, percentage):
    return {"type": "progressbar",
            "name": name,
            "percentage": percentage, }
