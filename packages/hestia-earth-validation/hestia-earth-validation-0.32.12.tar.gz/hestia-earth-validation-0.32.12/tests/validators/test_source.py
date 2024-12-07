import os
import json

from tests.utils import fixtures_path
from hestia_earth.validation.utils import _group_nodes
from hestia_earth.validation.validators.source import (
    validate_source,
    _validate_default_source
)

fixtures_folder = os.path.join(fixtures_path, 'source')
class_path = 'hestia_earth.validation.validators.source'


def test_validate_valid():
    with open(f"{fixtures_path}/source/valid.json") as f:
        node = json.load(f)
    results = validate_source(node)
    assert all([r is True for r in results])


def test_validate_default_source_valid():
    with open(f"{fixtures_folder}/defaultSource/source.json") as f:
        source = json.load(f)
    with open(f"{fixtures_folder}/defaultSource/valid.json") as f:
        nodes = json.load(f).get('nodes')
    assert _validate_default_source(source, _group_nodes(nodes)) is True

    # no other ndoes is valid
    assert _validate_default_source(source, _group_nodes([source])) is True


def test_validate_default_source_invalid():
    with open(f"{fixtures_folder}/defaultSource/source.json") as f:
        source = json.load(f)
    with open(f"{fixtures_folder}/defaultSource/invalid.json") as f:
        nodes = json.load(f).get('nodes')
    assert _validate_default_source(source, _group_nodes(nodes)) == {
        'level': 'error',
        'dataPath': '',
        'message': 'must be linked via a defaultSource'
    }
