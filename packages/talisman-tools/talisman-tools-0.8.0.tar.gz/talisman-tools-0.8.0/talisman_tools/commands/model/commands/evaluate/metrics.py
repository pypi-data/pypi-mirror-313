import math
from collections import defaultdict
from itertools import chain, starmap
from statistics import harmonic_mean, mean
from typing import Callable, Dict, Hashable, Iterable, List, NamedTuple, Sequence, Set, Tuple, Union

import numpy as np
from scipy.optimize import linear_sum_assignment


# copy of derek.common.evaluation.metrics


def f1_score(precision, recall):
    denominator = precision + recall
    return 2 * precision * recall / denominator if denominator > 0 else 0


def binary_precision_score(predicted: List[bool], gold: List[bool]):
    fp, fn, tp, tn = _compute_binary_errors(predicted, gold)
    denominator = tp + fp
    return tp / denominator if denominator > 0 else 0


def binary_recall_score(predicted: List[bool], gold: List[bool]):
    fp, fn, tp, tn = _compute_binary_errors(predicted, gold)
    denominator = tp + fn
    return tp / denominator if denominator > 0 else 0


def binary_f1_score(predicted: List[bool], gold: List[bool]):
    precision = binary_precision_score(predicted, gold)
    recall = binary_recall_score(predicted, gold)
    return f1_score(precision, recall)


def binary_accuracy(predicted: List[bool], gold: List[bool]):
    fp, fn, tp, tn = _compute_binary_errors(predicted, gold)
    denominator = tp + tn + fp + fn
    return (tp + tn) / denominator if denominator > 0 else 0


def binary_macro_avg_score(score_func, segments_predicted: List[List[bool]], segments_gold: List[List[bool]]):
    score = sum(score_func(pred, gold) for pred, gold in zip(segments_predicted, segments_gold))
    return score / len(segments_predicted) if len(segments_predicted) > 0 else 0


def binary_micro_avg_score(score_func, segments_predicted: List[List[bool]], segments_gold: List[List[bool]]):
    return score_func(list(chain.from_iterable(segments_predicted)), list(chain.from_iterable(segments_gold)))


def binary_macro_scores(segments_predicted: List[List[bool]], segments_gold: List[List[bool]]):
    macro_precision = binary_macro_avg_score(binary_precision_score, segments_predicted, segments_gold)
    macro_recall = binary_macro_avg_score(binary_recall_score, segments_predicted, segments_gold)
    macro_f1 = binary_macro_avg_score(binary_f1_score, segments_predicted, segments_gold)

    return macro_precision, macro_recall, macro_f1


def binary_micro_scores(segments_predicted: List[List[bool]], segments_gold: List[List[bool]]):
    micro_precision = binary_micro_avg_score(binary_precision_score, segments_predicted, segments_gold)
    micro_recall = binary_micro_avg_score(binary_recall_score, segments_predicted, segments_gold)
    micro_f1 = binary_micro_avg_score(binary_f1_score, segments_predicted, segments_gold)

    return micro_precision, micro_recall, micro_f1


def _compute_binary_errors(predicted: List[bool], gold: List[bool]):
    fp, fn, tp, tn = 0, 0, 0, 0

    for sample_pred, sample_gold in zip(predicted, gold):
        if sample_pred and sample_gold:
            tp += 1
        if sample_pred and not sample_gold:
            fp += 1
        if not sample_pred and sample_gold:
            fn += 1
        if not sample_pred and not sample_gold:
            tn += 1

    return fp, fn, tp, tn


def ir_precision_score(predicted: set, gold: set):
    return len(predicted.intersection(gold)) / len(predicted) if len(predicted) > 0 else 0


def ir_recall_score(predicted: set, gold: set):
    return len(predicted.intersection(gold)) / len(gold) if len(gold) > 0 else 0


def ir_f1_score(predicted: set, gold: set):
    intersection = predicted.intersection(gold)
    precision = len(intersection) / len(predicted) if len(predicted) > 0 else 0
    recall = len(intersection) / len(gold) if len(gold) > 0 else 0

    return f1_score(precision, recall)


def ir_macro_avg_score(score_func, segments_predicted: List[set], segments_gold: List[set]):
    score = 0

    for segment_predicted, segment_gold in zip(segments_predicted, segments_gold):
        score += score_func(segment_predicted, segment_gold)

    return score / len(segments_predicted) if len(segments_predicted) > 0 else 0


def ir_macro_scores(segments_predicted: List[set], segments_gold: List[set]):
    macro_precision = ir_macro_avg_score(ir_precision_score, segments_predicted, segments_gold)
    macro_recall = ir_macro_avg_score(ir_recall_score, segments_predicted, segments_gold)
    macro_f1 = ir_macro_avg_score(ir_f1_score, segments_predicted, segments_gold)

    return macro_precision, macro_recall, macro_f1


def ir_micro_avg_score(score_func, segments_predicted: List[set], segments_gold: List[set]):
    predicted = {(i, pred) for i, segment_pred in enumerate(segments_predicted) for pred in segment_pred}
    gold = {(i, gold) for i, segment_gold in enumerate(segments_gold) for gold in segment_gold}

    return score_func(predicted, gold)


def ir_micro_scores(segments_predicted: List[set], segments_gold: List[set]):
    predicted = {(i, pred) for i, segment_pred in enumerate(segments_predicted) for pred in segment_pred}
    gold = {(i, gold) for i, segment_gold in enumerate(segments_gold) for gold in segment_gold}

    micro_precision = ir_precision_score(predicted, gold)
    micro_recall = ir_recall_score(predicted, gold)
    micro_f1 = ir_f1_score(predicted, gold)

    return micro_precision, micro_recall, micro_f1


def ir_categorized_queries_score(
        queries: List,
        queries_predicted: List[set], queries_gold: List[set],
        categorizer: Callable, score_func: Callable):

    queries_predicted_filtered = []
    queries_gold_filtered = []
    possible_categories = set()

    for query, query_pred, query_gold in zip(queries, queries_predicted, queries_gold):
        filtered_pred = _categorize_query_objects(query, query_pred, categorizer)
        filtered_gold = _categorize_query_objects(query, query_gold, categorizer)

        queries_predicted_filtered.append(filtered_pred)
        queries_gold_filtered.append(filtered_gold)
        possible_categories.update(filtered_gold.keys(), filtered_pred.keys())

    categories_results = {}

    for category in possible_categories:
        # defaultdict provide empty set if category is not present in query
        category_predicted = [query_pred[category] for query_pred in queries_predicted_filtered]
        category_gold = [query_gold[category] for query_gold in queries_gold_filtered]

        category_score = score_func(category_predicted, category_gold)
        categories_results[category] = category_score

    return categories_results


def _categorize_query_objects(query, objects: set, categorizer: Callable) -> defaultdict:
    filtered_objects = defaultdict(set)

    for obj in objects:
        filtered_objects[categorizer(query, obj)].add(obj)

    return filtered_objects


def reciprocal_rank(relevant: Union[set, frozenset], ranked_responses: Sequence) -> float:
    for i, obj in enumerate(ranked_responses, start=1):
        if obj in relevant:
            return 1 / i
    return 0.0


def mean_reciprocal_rank(segments_predicted: Sequence[Sequence], segments_gold: Sequence[Union[set, frozenset]]) -> float:
    if len(segments_predicted) != len(segments_gold):
        raise ValueError("Segments must be aligned")

    macro_sum = sum(starmap(reciprocal_rank, zip(segments_gold, segments_predicted)), 0.0)
    return macro_sum / len(segments_predicted) if len(segments_predicted) else 0.0


# following this are coreference metrics adapted from scorch 0.2.0

def _trace(cluster: Set, partition: Iterable[Set]) -> Iterable[Set]:
    r"""
    Return the partition of `#cluster` induced by `#partition`, that is
    ```math
    \{C∩A|A∈P\} ∪ \{\{x\}|x∈C∖∪P\}
    ```
    Where `$C$` is `#cluster` and `$P$` is `#partition`.
    This assume that the elements of `#partition` are indeed pairwise disjoint.
    """
    remaining = set(cluster)
    for a in partition:
        common = remaining.intersection(a)
        if common:
            remaining.difference_update(common)
            yield common
    for x in sorted(remaining):
        yield {x}


class RemapClusteringsReturn(NamedTuple):
    clusterings: Sequence[Sequence[Sequence[int]]]
    elts_map: Dict[Hashable, int]


def remap_clusterings(
    clusterings: Sequence[Sequence[Set[Hashable]]],
) -> RemapClusteringsReturn:
    """Remap clusterings of arbitrary elements to clusterings of integers."""
    elts = {e for clusters in clusterings for c in clusters for e in c}
    elts_map = {e: i for i, e in enumerate(elts)}
    res = []
    for clusters in clusterings:
        remapped_clusters = []
        for c in clusters:
            remapped_c = [elts_map[e] for e in c]
            remapped_clusters.append(remapped_c)
        res.append(remapped_clusters)
    return RemapClusteringsReturn(res, elts_map)


def muc_score(key: Sequence[Set], response: Sequence[Set]) -> Tuple[float, float, float]:
    r"""
        Compute the MUC `$(R, P, F₁)$` scores for a `#response` clustering given a `#key` clustering,
        that is
        ```math
        R &= \frac{∑_{k∈K}(\#k-\#p(k, R))}{∑_{k∈K}(\#k-1)}\\
        P &= \frac{∑_{r∈R}(\#r-\#p(r, K))}{∑_{r∈R}(\#r-1)}\\
        F &= 2*\frac{PR}{P+R}
        ```
        with `$p(x, E)=\{x∩A|A∈E\}$`.
        In the edge case where all clusters in either `#key` or `#response` are singletons, `$P$`, `$R$`
        and `$F$` are defined to be `$0$`, following the reference implementation (since singleton
        clusters where not considered in Vilain et al. (1995).
        Note: This implementation is significantly different from the reference one (despite
        implementing the formulae from Pradahan et al. (2014) in that the reference use the ordering of
        mentions in documents to consistently assign a non-problematic spanning tree (viz. a chain) to
        each cluster, thus avoiding the issues that led Vilain et al. (1995) to define MUC by the
        formulae above.
        """
    # Edge case
    if all(len(k) == 1 for k in key) or all(len(r) == 1 for r in response):
        return 0.0, 0.0, 0.0

    def func(one: Sequence[Set], another: Sequence[Set]):
        return sum(len(o) - sum(1 for _ in _trace(o, another)) for o in one) / sum(len(o) - 1 for o in one)

    r = func(key, response)
    p = func(response, key)
    f = harmonic_mean((float(r), float(p)))
    return r, p, f


def bcub_score(
    key: Sequence[Set], response: Sequence[Set]
) -> Tuple[float, float, float]:
    r"""
    Compute the B³ `$(R, P, F₁)$` scores for a `#response` clustering given a `#key` clustering,
    that is
    ```math
    R &= \frac{∑_{k∈K}∑_{r∈R}\frac{(\#k∩r)²}{\#k}}{∑_{k∈K}\#k}\\
    P &= \frac{∑_{r∈R}∑_{k∈K}\frac{(\#r∩k)²}{\#r}}{∑_{r∈R}\#r}\\
    F &= 2*\frac{PR}{P+R}
    ```
    """

    def func(one, another):
        if sum(map(len, one)) == 0:
            return 0.0
        return math.fsum(len(o.intersection(a)) ** 2 / len(o) for o in one for a in another) / sum(len(o) for o in one)

    r = func(key, response)
    p = func(response, key)
    f = harmonic_mean((float(r), float(p)))
    return r, p, f


def ceaf_score(
    key: Sequence[Set],
    response: Sequence[Set],
    score: Callable[[Set, Set], float],
) -> Tuple[float, float, float]:
    r"""
    Compute the CEAF `$(R, P, F₁)$` scores for a `#response` clustering given a `#key` clustering
    using the `#score` alignment score function, that is
    ```math
    R &= \frac{∑_{k∈K}C(k, A(k))}{∑_{k∈K}C(k, k)}\\
    P &= \frac{∑_{r∈R}C(r, A⁻¹(r))}{∑_{r∈R}C(r, r)}\\
    F &= 2*\frac{PR}{P+R}
    ```
    Where `$C$` is `#score` and `$A$` is a one-to-one mapping from key clusters to response
    clusters that maximizes `$∑_{k∈K}C(k, A(k))$`.
    """
    if len(response) == 0 or len(key) == 0:
        return 0.0, 0.0, 0.0
    else:
        cost_matrix = np.array([[-score(k, r) for r in response] for k in key])
        # TODO: See https://github.com/allenai/allennlp/issues/2946 for ideas on speeding
        # the next line up
        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        total_score = -cost_matrix[row_ind, col_ind].sum()
        r = total_score / math.fsum(score(k, k) for k in key)
        p = total_score / math.fsum(score(res, res) for res in response)
        f = harmonic_mean((float(r), float(p)))
        return r, p, f


def ceafe_score(
    key: Sequence[Set], response: Sequence[Set]
) -> Tuple[float, float, float]:
    r"""
    Compute the CEAFₑ `$(R, P, F₁)$` scores for a `#response` clustering given a `#key`
    clustering, that is the CEAF score for the `$Φ₄$` score function (aka the Sørensen–Dice
    coefficient).
    ```math
    Φ₄: (k, r) ⟼ \frac{2×\#k∩r}{\#k+\#r}
    ```
    Note: this use the original (Luo, 2005) definition as opposed to Pradhan et al. (2014)'s one
    which inlines the denominators.
    """

    def theta_4(k, r):
        return 2 * len(k.intersection(r)) / (len(k) + len(r))

    return ceaf_score(key, response, theta_4)


def conll2012_score(key: Sequence[Set], response: Sequence[Set]) -> float:
    r"""
    Return the CoNLL-2012 scores for a `#response` clustering given a `#key` clustering, that is,
    the average of the MUC, B³ and CEAFₑ scores.
    """
    return mean((metric(key, response)[2] for metric in (muc_score, bcub_score, ceafe_score)))

# lea section adapted from CoVal at github.com/ns-moosavi/coval


def get_mention_assignments(in_clusters, out_clusters):
    mention_cluster_ids = {}
    res = {}
    for ix, cluster in enumerate(out_clusters):
        for mention in cluster:
            res[mention] = ix

    for cluster in in_clusters:
        for mention in cluster:
            if mention in res:
                mention_cluster_ids[mention] = res[mention]

    return mention_cluster_ids


def lea_score(key: Sequence[Set], response: Sequence[Set]):
    listify = lambda seq: [list(x) for x in seq]
    lkey = listify(key)
    lresponse = listify(response)
    key_mention_assignment = get_mention_assignments(lkey, lresponse)
    res_mention_assignment = get_mention_assignments(lresponse, lkey)
    pn, pd = lea(lresponse, lkey, res_mention_assignment)
    rn, rd = lea(lkey, lresponse, key_mention_assignment)
    p = 0 if pd == 0 else pn / float(pd)
    r = 0 if rd == 0 else rn / float(rd)
    f1 = 0 if p + r == 0 else 2 * p * r / (p + r)

    return r, p, f1


def lea(input_clusters, output_clusters, mention_to_gold):
    num, den = 0, 0

    for c in input_clusters:
        if len(c) == 1:
            all_links = 1
            if c[0] in mention_to_gold and len(
                    output_clusters[mention_to_gold[c[0]]]) == 1:
                common_links = 1
            else:
                common_links = 0
        else:
            common_links = 0
            all_links = len(c) * (len(c) - 1) / 2.0
            for i, m in enumerate(c):
                if m in mention_to_gold:
                    for m2 in c[i + 1:]:
                        if m2 in mention_to_gold and mention_to_gold[
                                m] == mention_to_gold[m2]:
                            common_links += 1

        num += len(c) * common_links / float(all_links)
        den += len(c)

    return num, den
