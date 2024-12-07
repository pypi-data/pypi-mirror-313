from .shared import (
    validate_date_lt_today
)


def _validate_default_source(source: dict, node_map: dict = {}):
    # prevent adding a source that is not a `defaultSource` of another Node
    is_new_source = 'id' in source
    node_types = list(filter(lambda t: t != 'Source' and t != 'Actor', node_map.keys()))
    # uploading only sources is valid too
    has_other_nodes = len(node_types) > 0
    has_default_source = any([
        node.get('defaultSource', {}).get('id') == source.get('id')
        for values in node_map.values()
        for node in values.values()
    ]) if is_new_source else True
    return source.get('dataPrivate', True) or not has_other_nodes or has_default_source or {
        'level': 'error',
        'dataPath': '',
        'message': 'must be linked via a defaultSource'
    }


def validate_source(source: dict, node_map: dict = {}):
    """
    Validates a single `Organisation`.

    Parameters
    ----------
    organisation : dict
        The `Organisation` to validate.
    node_map : dict
        The list of all nodes to do cross-validation, grouped by `type` and `id`.

    Returns
    -------
    List
        The list of errors for the `Organisation`, which can be empty if no errors detected.
    """
    return [
        validate_date_lt_today(source, 'bibliography.year'),
        _validate_default_source(source, node_map)
    ]
