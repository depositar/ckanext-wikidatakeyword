from ckan.common import json
from ckan.plugins.toolkit import missing, _


def wikidata_keyword(key, data, errors, context):
    """
    Accept wikidata keywords input in the following forms
    and convert to a json list for storage:

    1. a list of wikidata ids, eg.
       ["Q1", "Q2"]

    2. a single comma separated string with wikidata ids, eg.
       "Q1, Q2"
    """
    if errors[key]:
        return

    value = data[key]
    if value is not missing:
        if isinstance(data[key], basestring):
            value = [element.strip()
                     for element in value.split(',')
                     if element.strip()]
        if not isinstance(value, list):
            errors[key].append(_('expecting list of strings'))
            return
    else:
        value = []

    if not errors[key]:
        data[key] = json.dumps(value)

    return


def wikidata_keyword_output(value):
    """
    return stored json as a proper list
    """
    if isinstance(value, list):
        return value
    try:
        return json.loads(value)
    except ValueError:
        return [value]
