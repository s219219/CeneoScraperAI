def extractElement(ancestor, selector, attribute=None):
    try:
        if attribute:
            return ancestor.select(selector).pop(0)[attribute].strip()
        else:
            return ancestor.select(selector).pop(0).text.strip()
    except IndexError:
        return None