import json
from unittest.mock import patch
from hestia_earth.schema import SiteSiteType, TermTermType

from tests.utils import FUEL_TERM_IDS, fixtures_path, fake_get_terms
from hestia_earth.validation.validators.completeness import (
    validate_completeness,
    _validate_all_values,
    _validate_cropland,
    _validate_material,
    _validate_freshForage,
    _validate_ingredient
)

class_path = 'hestia_earth.validation.validators.completeness'


@patch(f"{class_path}.get_terms", side_effect=fake_get_terms)
def test_validate_completeness_valid(*args):
    with open(f"{fixtures_path}/completeness/valid.json") as f:
        data = json.load(f)
    assert validate_completeness({'completeness': data}) is True


def test_validate_all_values_valid():
    with open(f"{fixtures_path}/completeness/valid.json") as f:
        data = json.load(f)
    assert _validate_all_values(data) is True


def test_validate_all_values_warning():
    with open(f"{fixtures_path}/completeness/all-values/warning.json") as f:
        data = json.load(f)
    assert _validate_all_values(data) == {
        'level': 'warning',
        'dataPath': '.completeness',
        'message': 'may not all be set to false'
    }


def test_validate_cropland_valid():
    with open(f"{fixtures_path}/completeness/cropland/site.json") as f:
        site = json.load(f)
    with open(f"{fixtures_path}/completeness/cropland/valid.json") as f:
        data = json.load(f)
    assert _validate_cropland(data, site) is True

    # also works if siteType is not cropland
    site['siteType'] = SiteSiteType.LAKE.value
    data[TermTermType.EXCRETA.value] = False
    assert _validate_cropland(data, site) is True


def test_validate_cropland_warning():
    with open(f"{fixtures_path}/completeness/cropland/site.json") as f:
        site = json.load(f)
    with open(f"{fixtures_path}/completeness/cropland/warning.json") as f:
        data = json.load(f)
    assert _validate_cropland(data, site) == [
        {
            'level': 'warning',
            'dataPath': '.completeness.animalFeed',
            'message': 'should be true for site of type cropland'
        },
        {
            'level': 'warning',
            'dataPath': '.completeness.excreta',
            'message': 'should be true for site of type cropland'
        }
    ]


@patch(f"{class_path}.get_terms", side_effect=fake_get_terms)
def test_validate_material_valid(*args):
    with open(f"{fixtures_path}/completeness/material/valid-incomplete.json") as f:
        data = json.load(f)
    assert _validate_material(data) is True

    with open(f"{fixtures_path}/completeness/material/valid-no-fuel.json") as f:
        data = json.load(f)
    assert _validate_material(data) is True

    with open(f"{fixtures_path}/completeness/material/valid-fuel-material.json") as f:
        data = json.load(f)
    assert _validate_material(data) is True


@patch(f"{class_path}.get_terms", side_effect=fake_get_terms)
def test_validate_material_error(*args):
    with open(f"{fixtures_path}/completeness/material/error.json") as f:
        data = json.load(f)
    assert _validate_material(data) == {
        'level': 'error',
        'dataPath': '.completeness.material',
        'message': 'must be set to false when specifying fuel use',
        'params': {
            'allowedValues': FUEL_TERM_IDS
        }
    }


@patch(f"{class_path}.get_terms", side_effect=fake_get_terms)
def test_validate_freshForage_valid(*args):
    with open(f"{fixtures_path}/completeness/freshForage/valid-animals.json") as f:
        data = json.load(f)
    assert _validate_freshForage(data, data.get('site')) is True

    with open(f"{fixtures_path}/completeness/freshForage/valid-animal-inputs.json") as f:
        data = json.load(f)
    assert _validate_freshForage(data, data.get('site')) is True

    with open(f"{fixtures_path}/completeness/freshForage/valid-products.json") as f:
        data = json.load(f)
    assert _validate_freshForage(data, data.get('site')) is True

    with open(f"{fixtures_path}/completeness/freshForage/valid-not-liveAnimal.json") as f:
        data = json.load(f)
    assert _validate_freshForage(data, data.get('site')) is True

    with open(f"{fixtures_path}/completeness/freshForage/valid-not-grazing-liveAnimal.json") as f:
        data = json.load(f)
    assert _validate_freshForage(data, data.get('site')) is True


@patch(f"{class_path}.get_terms", side_effect=fake_get_terms)
def test_validate_freshForage_error(*args):
    with open(f"{fixtures_path}/completeness/freshForage/error-animals.json") as f:
        data = json.load(f)
    assert _validate_freshForage(data, data.get('site')) == {
        'level': 'error',
        'dataPath': '.completeness.freshForage',
        'message': 'must have inputs representing the forage when set to true',
        'params': {
            'siteType': 'permanent pasture'
        }
    }

    with open(f"{fixtures_path}/completeness/freshForage/error-products.json") as f:
        data = json.load(f)
    assert _validate_freshForage(data, data.get('site')) == {
        'level': 'error',
        'dataPath': '.completeness.freshForage',
        'message': 'must have inputs representing the forage when set to true',
        'params': {
            'siteType': 'permanent pasture'
        }
    }


@patch(f"{class_path}.get_terms", side_effect=fake_get_terms)
def test_validate_ingredient_valid(*args):
    with open(f"{fixtures_path}/completeness/ingredient/valid.json") as f:
        data = json.load(f)
    assert _validate_ingredient(data, data.get('site')) is True

    with open(f"{fixtures_path}/completeness/ingredient/valid-agri-food-processor-complete.json") as f:
        data = json.load(f)
    assert _validate_ingredient(data, data.get('site')) is True

    with open(f"{fixtures_path}/completeness/ingredient/valid-agri-food-processor-incomplete.json") as f:
        data = json.load(f)
    assert _validate_ingredient(data, data.get('site')) is True


@patch(f"{class_path}.get_terms", side_effect=fake_get_terms)
def test_validate_ingredient_error(*args):
    with open(f"{fixtures_path}/completeness/ingredient/invalid.json") as f:
        data = json.load(f)
    assert _validate_ingredient(data, data.get('site')) == {
        'level': 'error',
        'dataPath': '.completeness.ingredient',
        'message': 'ingredients should be complete',
        'params': {
            'siteType': 'cropland'
        }
    }

    with open(f"{fixtures_path}/completeness/ingredient/invalid-agri-food-processor.json") as f:
        data = json.load(f)
    assert _validate_ingredient(data, data.get('site')) == {
        'level': 'error',
        'dataPath': '.completeness.ingredient',
        'message': 'must have inputs to represent ingredients',
        'params': {
            'siteType': 'agri-food processor'
        }
    }
