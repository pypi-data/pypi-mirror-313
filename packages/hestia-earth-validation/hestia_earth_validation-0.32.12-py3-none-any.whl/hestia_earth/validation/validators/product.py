import traceback
from hestia_earth.schema import TermTermType, CycleFunctionalUnit
from hestia_earth.utils.model import find_primary_product, filter_list_term_type
from hestia_earth.utils.lookup import get_table_value, download_lookup, column_name
from hestia_earth.utils.tools import list_sum, flatten, non_empty_list
from hestia_earth.distribution.posterior_yield import get_post
from hestia_earth.distribution.prior_yield import get_prior

from hestia_earth.validation.log import logger
from hestia_earth.validation.utils import _list_sum, _filter_list_errors
from hestia_earth.validation.distribution import UNIVARIATE_DEFAULT_THRESHOLD, validate as validate_distribution
from .shared import CROP_SITE_TYPE


def validate_economicValueShare(products: list):
    sum = _list_sum(products, 'economicValueShare')
    return sum <= 100.5 or {
        'level': 'error',
        'dataPath': '.products',
        'message': 'economicValueShare should sum to 100 or less across all products',
        'params': {
            'sum': sum
        }
    }


def validate_value_empty(products: list):
    def validate(values: tuple):
        index, product = values
        return len(product.get('value', [])) > 0 or {
            'level': 'warning',
            'dataPath': f".products[{index}]",
            'message': 'may not be 0'
        }

    return _filter_list_errors(map(validate, enumerate(products)))


def validate_value_0(products: list):
    def validate(values: tuple):
        index, product = values
        value = list_sum(product.get('value', [-1]), -1)
        eva = product.get('economicValueShare', 0)
        revenue = product.get('revenue', 0)
        return value != 0 or _filter_list_errors([
            eva == 0 or {
                'level': 'error',
                'dataPath': f".products[{index}].value",
                'message': 'economicValueShare must be 0 for product value 0',
                'params': {
                    'value': eva,
                    'term': product.get('term')
                }
            },
            revenue == 0 or {
                'level': 'error',
                'dataPath': f".products[{index}].value",
                'message': 'revenue must be 0 for product value 0',
                'params': {
                    'value': revenue,
                    'term': product.get('term')
                }
            }
        ])

    return _filter_list_errors(flatten(map(validate, enumerate(products))))


MAX_PRIMARY_PRODUCTS = 1


def validate_primary(products: list):
    primary = list(filter(lambda p: p.get('primary', False), products))
    return len(primary) <= MAX_PRIMARY_PRODUCTS or {
        'level': 'error',
        'dataPath': '.products',
        'message': f"only {MAX_PRIMARY_PRODUCTS} primary product allowed"
    }


def _get_excreta_term(lookup, product_id: str, column: str):
    value = get_table_value(lookup, 'termid', product_id, column_name(column))
    return non_empty_list((value or '').split(';'))


UNITS_TO_EXCRETA_LOOKUP = {
    'kg': ['allowedExcretaKgMassTermIds', 'recommendedExcretaKgMassTermIds'],
    'kg N': ['allowedExcretaKgNTermIds', 'recommendedExcretaKgNTermIds'],
    'kg VS': ['allowedExcretaKgVsTermIds', 'recommendedExcretaKgVsTermIds']
}


def validate_excreta(cycle: dict, list_key: str = 'products'):
    primary_product = find_primary_product(cycle) or {}
    product_term_id = primary_product.get('term', {}).get('@id')
    lookup = download_lookup(f"{primary_product.get('term', {}).get('termType')}.csv")

    def validate(values: tuple):
        index, product = values
        term_id = product.get('term', {}).get('@id')
        term_type = product.get('term', {}).get('termType')
        term_units = product.get('term', {}).get('units')
        allowed_column, recommended_column = UNITS_TO_EXCRETA_LOOKUP.get(term_units, [None, None])
        allowed_ids = _get_excreta_term(lookup, product_term_id, allowed_column)
        recommended_ids = _get_excreta_term(lookup, product_term_id, recommended_column)
        return term_type != TermTermType.EXCRETA.value or (
            len(allowed_ids) != 0 and term_id not in allowed_ids and {
                'level': 'error',
                'dataPath': f".{list_key}[{index}].term.@id",
                'message': 'is too generic',
                'params': {
                    'product': primary_product.get('term'),
                    'term': product.get('term', {}),
                    'current': term_id,
                    'expected': allowed_ids
                }
            }
        ) or (
            len(recommended_ids) != 0 and term_id not in recommended_ids and {
                'level': 'warning',
                'dataPath': f".{list_key}[{index}].term.@id",
                'message': 'is too generic',
                'params': {
                    'product': primary_product.get('term'),
                    'term': product.get('term', {}),
                    'current': term_id,
                    'expected': recommended_ids
                }
            }
        ) or True

    return _filter_list_errors(map(validate, enumerate(cycle.get(list_key, []))))


def validate_product_ha_functional_unit_ha(cycle: dict, list_key: str = 'products'):
    functional_unit = cycle.get('functionalUnit', CycleFunctionalUnit.RELATIVE.value)

    def validate(values: tuple):
        index, product = values
        term_units = product.get('term', {}).get('units')
        value = list_sum(product.get('value', [0]))
        return term_units != 'ha' or value <= 1 or {
            'level': 'error',
            'dataPath': f".{list_key}[{index}].value",
            'message': 'must be below or equal to 1 for unit in ha',
            'params': {
                'term': product.get('term', {})
            }
        }

    return functional_unit != CycleFunctionalUnit._1_HA.value or \
        _filter_list_errors(map(validate, enumerate(cycle.get(list_key, []))))


def _validate_product_yield(country: dict, list_key: str, threshold: float):
    country_id = country.get('@id')

    def validate(values: tuple):
        index, product = values

        product_id = product.get('term', {}).get('@id')
        product_value = product.get('value', [])

        def _get_mu_sd():
            mu, sd = get_post(country_id, product_id)
            return (mu, sd) if mu is not None else get_prior(country_id, product_id)

        valid, outliers, min, max = validate_distribution(product_value, threshold, get_mu_sd=_get_mu_sd)
        return valid or {
            'level': 'warning',
            'dataPath': f".{list_key}[{index}].value",
            'message': 'is outside confidence interval',
            'params': {
                'term': product.get('term', {}),
                'country': country,
                'outliers': outliers,
                'threshold': threshold,
                'min': min,
                'max': max
            }
        }
    return validate


def validate_product_yield(
    cycle: dict, site: dict, list_key: str = 'products', threshold: float = UNIVARIATE_DEFAULT_THRESHOLD
):
    country = site.get('country', {})
    products = cycle.get(list_key, [])

    try:
        return site.get('siteType') not in CROP_SITE_TYPE or (
            _filter_list_errors(map(_validate_product_yield(country, list_key, threshold), enumerate(products)))
        )
    except Exception:
        stack = traceback.format_exc()
        logger.error(f"Error validating using distribution: '{stack}'")
        return True


def validate_liveAnimal_requires_excreta(cycle: dict, list_key: str = 'products'):
    products = cycle.get(list_key, [])
    has_liveAnimal = len(filter_list_term_type(products, TermTermType.LIVEANIMAL)) > 0
    has_excreta = len(filter_list_term_type(products, TermTermType.EXCRETA)) > 0
    return not has_liveAnimal or has_excreta or {
        'level': 'error',
        'dataPath': f".{list_key}",
        'message': 'must add an excreta product with a liveAnimal product'
    }
