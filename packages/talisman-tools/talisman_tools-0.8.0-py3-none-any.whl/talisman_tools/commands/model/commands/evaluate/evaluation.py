from collections import defaultdict
from itertools import zip_longest
from typing import Any, Callable, Iterable

from tdm import TalismanDocument

from .metrics import ir_categorized_queries_score, ir_macro_scores, ir_micro_scores


def _scores2dict(precision: float, recall: float, f1: float):
    return {"precision": float(precision), "recall": float(recall), "f1": float(f1)}


def _with_prefix(d: dict[str, Any], prefix: str) -> dict:
    return {f"{prefix}_{k}": v for k, v in d.items()}


def _evaluate(
        predicted: Iterable[TalismanDocument],
        gold: Iterable[TalismanDocument],
        objects_getter: Callable[[TalismanDocument], Iterable[Any]],
        categorizers: dict[str, Callable]
) -> dict[str, dict]:

    queries = []
    predicted_objects, gold_objects = [], []

    for pred_doc, gold_doc in zip_longest(predicted, gold):

        if pred_doc is None or gold_doc is None:
            raise ValueError('Predicted and gold documents iterables length mismatch')

        if pred_doc.id != gold_doc.id:
            raise ValueError(f'The document sequences are not identical {pred_doc.id} != {gold_doc.id}')

        if pred_doc.main_root.content != gold_doc.main_root.content:
            raise ValueError('Predicted and gold documents have different texts')

        predicted_objects.append(set(objects_getter(pred_doc)))
        gold_objects.append(set(objects_getter(gold_doc)))
        queries.append(gold_doc.main_root.content)

    macro_scores = _scores2dict(*ir_macro_scores(predicted_objects, gold_objects))
    micro_scores = _scores2dict(*ir_micro_scores(predicted_objects, gold_objects))
    final_scores = {**_with_prefix(macro_scores, 'macro'), **_with_prefix(micro_scores, 'micro'), 'categories': {}}

    for categorizer_name, categorizer in categorizers.items():
        category_scores = defaultdict(dict)

        for strategy_name, strategy in [('micro', ir_micro_scores), ('macro', ir_macro_scores)]:
            scores: dict[str, tuple[float, float, float]] = ir_categorized_queries_score(
                queries, predicted_objects, gold_objects, categorizer, strategy)
            scores: dict[str, dict[str, float]] = {k: _with_prefix(_scores2dict(*vals), strategy_name) for k, vals in scores.items()}
            for key, val in scores.items():
                category_scores[key].update(val)

        final_scores['categories'][categorizer_name] = dict(category_scores)

    return final_scores


def evaluate_categorized_objects(predicted_objects: dict[str, list[set]], gold_objects: dict[str, list[set]]) -> dict[str, dict]:
    num_groups_in_predicted_categories = list(map(len, predicted_objects.values()))
    num_groups_in_gold_categories = list(map(len, gold_objects.values()))

    if num_groups_in_gold_categories != num_groups_in_predicted_categories:
        raise ValueError('Predicted and gold category groups should match!')

    if predicted_objects.keys() != gold_objects.keys():
        raise ValueError('Predicted and gold categories should match!')

    if not len(num_groups_in_predicted_categories):
        raise ValueError('There should be at least one category!')

    num_groups = num_groups_in_predicted_categories[0]
    if any(ng != num_groups for ng in num_groups_in_predicted_categories):
        raise ValueError('Each category should have the same number of groups!')

    uncategorized_predicted_objects: list[set] = [set() for _ in range(num_groups)]
    uncategorized_gold_objects: list[set] = [set() for _ in range(num_groups)]

    for category in predicted_objects.keys():
        category_predicted_objects = predicted_objects[category]
        category_gold_objects = gold_objects[category]

        def categorize(obj) -> tuple:
            return category, obj

        for collected_group_objects, group_objects in zip(uncategorized_predicted_objects, category_predicted_objects):
            collected_group_objects.update(map(categorize, group_objects))
        for collected_group_objects, group_objects in zip(uncategorized_gold_objects, category_gold_objects):
            collected_group_objects.update(map(categorize, group_objects))

    macro_scores = _scores2dict(*ir_macro_scores(uncategorized_predicted_objects, uncategorized_gold_objects))
    micro_scores = _scores2dict(*ir_micro_scores(uncategorized_predicted_objects, uncategorized_gold_objects))
    final_scores = {**_with_prefix(macro_scores, 'macro'), **_with_prefix(micro_scores, 'micro'), 'categories': {}}

    for category in gold_objects.keys():
        macro_scores = _scores2dict(*ir_macro_scores(predicted_objects[category], gold_objects[category]))
        micro_scores = _scores2dict(*ir_micro_scores(predicted_objects[category], gold_objects[category]))
        final_scores['categories'][category] = {**_with_prefix(macro_scores, 'macro'), **_with_prefix(micro_scores, 'micro')}

    return final_scores
