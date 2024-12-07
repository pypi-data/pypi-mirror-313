import os
import math

ENABLED = os.getenv('VALIDATE_DISTRIBUTION', 'true') == 'true'

UNIVARIATE_DEFAULT_THRESHOLD = 0.95
UNIVARIATE_DEFAULT_ZSCORE = 1.96
UNIVARIATE_CI_TO_ZSCORE = {
    0.9: 1.65,
    UNIVARIATE_DEFAULT_THRESHOLD: UNIVARIATE_DEFAULT_ZSCORE,
    0.99: 2.58
}


def validate(values: list, threshold: float, get_mu_sd):
    def exec():
        z = UNIVARIATE_CI_TO_ZSCORE[threshold]
        mu, sd = get_mu_sd()
        _min = mu-(z*sd) if mu is not None else None
        _max = mu+(z*sd) if mu is not None else None
        passes = [_min <= y <= _max if all([mu is not None, not math.isnan(y)]) else True for y in values]
        outliers = [y for y in values if not _min <= y <= _max] if mu is not None else []
        return all(passes), outliers, max(_min or 0, 0), _max
    return exec() if ENABLED else (True, [], None, None)
