

def label(*lines, **kwargs):
    return {"type": "label",
            "name": kwargs.get("name"),
            "text": "\n".join(lines), }


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
