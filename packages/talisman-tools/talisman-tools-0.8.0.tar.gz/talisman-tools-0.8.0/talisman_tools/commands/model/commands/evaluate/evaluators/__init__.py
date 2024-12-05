from functools import partial

from .disambiguation_quality import evaluate_dmb
from .nerc import evaluate_nerc
from .relext import evaluate_relext, evaluate_relext_upper_bound


evaluators = {
    'all': {
        'nerc': evaluate_nerc,
        'relext': evaluate_relext,
        'relext-upper-bound': evaluate_relext_upper_bound,
        'dmb': partial(evaluate_dmb, at_ks=[1, 2, 3])  # TODO: make configurable from cli
    },
    'relext': {
        'relext': evaluate_relext
    },
    'nerc': {
        'nerc': evaluate_nerc
    },
    'dmb': {
        'dmb': partial(evaluate_dmb, at_ks=[1, 2, 3])  # TODO: make configurable from cli
    },
    # 'coref': {
    #     'coref': evaluate_coref
    # }
}
