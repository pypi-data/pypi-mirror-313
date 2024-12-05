from typing import Callable, Dict, List, Sequence, Tuple

from tdm import TalismanDocument
from tdm.datamodel.facts import ConceptFact

from talisman_tools.commands.model.commands.evaluate.metrics import ir_micro_avg_score, ir_recall_score, mean_reciprocal_rank


def _compute_micro_recall_at_k(predicted: List[tuple], gold: List[set], k: int) -> float:
    if k <= 0:
        raise ValueError(f"{k} must be > 0")

    predicted_at_k = [set(s[:k]) for s in predicted]
    return ir_micro_avg_score(ir_recall_score, predicted_at_k, gold)


_Predicate = Callable[[ConceptFact], bool]


def _truth_predicate(fact: ConceptFact) -> bool:
    return True


def _in_kb_predicate(fact: ConceptFact) -> bool:
    return fact.value is not None and fact.value


def _ambiguity_predicate(fact: ConceptFact) -> bool:
    return fact.value is not None and isinstance(fact.value, tuple) and len(fact.value) >= 2


def _filter_with_mode(predicted: Sequence[TalismanDocument], gold: Sequence[TalismanDocument], only_in_kb: bool, mode: str) -> \
        Tuple[Sequence[TalismanDocument], Sequence[TalismanDocument]]:

    if mode == "default" and not only_in_kb:
        return predicted, gold

    gold_predicate = _in_kb_predicate if only_in_kb else _truth_predicate
    if mode == "default":
        pred_predicate = _truth_predicate
    elif mode == "ambigous":
        pred_predicate = _ambiguity_predicate
    elif mode == "unambigous":
        pred_predicate = lambda fact: not _ambiguity_predicate(fact)
    else:
        raise ValueError(f"{mode} is not supported")

    pred_filtered, gold_filtered = [], []
    for pred_doc, gold_doc in zip(predicted, gold):
        pred_facts = tuple(pred_doc.filter_facts(ConceptFact, pred_predicate))
        gold_facts = tuple(gold_doc.filter_facts(ConceptFact, gold_predicate))

        mentions_intersection = {fact.mention for fact in pred_facts}.intersection(fact.mention for fact in gold_facts)

        pred_filtered.append(pred_doc.without_facts().with_facts(fact for fact in pred_facts if fact.mention in mentions_intersection))
        gold_filtered.append(gold_doc.without_facts().with_facts(fact for fact in gold_facts if fact.mention in mentions_intersection))

    return pred_filtered, gold_filtered


def is_ambiguous(doc: TalismanDocument) -> bool:  # TODO: move it to helpers/tdm
    return any(isinstance(fact.value, tuple) and fact.value for fact in doc.facts[ConceptFact])


def _group_facts(doc: TalismanDocument) -> Dict[tuple, ConceptFact]:
    result = {}
    for fact in doc.facts[ConceptFact]:
        key = fact.type_id, fact.mention
        if key in result:
            raise ValueError
        result[key] = fact
    return result


def evaluate_dmb(
        predicted: Sequence[TalismanDocument], gold: Sequence[TalismanDocument], eval_config: dict, at_ks: Sequence[int],
        only_in_kb: bool = False, mode: str = "default") -> Dict[str, float]:
    """
    :param predicted: Sequence of disambiguated Documents with ranked concept fact values ranked_concepts
    :param gold: Sequence of unambiguous Documents with gold concept fact values
    :param eval_config: optional evaluation config
    :param at_ks: Compute micro_recall@k for all k from at_ks
    :param only_in_kb: Evaluate only in KB mentions
    :param mode: "default" | "ambiguous" | "non_ambigous".
        If "default", evaluate all mentions.
        If "ambigous" evaluate only ambigous mentions (with at least 2 predicted concepts)
        If "unambigous" evaluate only unambigous mentions (with at most 1 predicted concept)
    :return: dictionary with keys:
        "num_mentions" -- number of evaluated mentions
        "micro_recall@k" -- value of micro_recall at k for each k from at_ks param
        "mean_reciprocal_rank" -- value of mean reciprocal rank
    """
    if len(predicted) != len(gold):
        raise ValueError("Predicted and gold sequences are not aligned")
    if any(map(is_ambiguous, gold)):
        raise ValueError("Gold sequence contains ambiguous documents")

    predicted, gold = _filter_with_mode(predicted, gold, only_in_kb, mode)

    def response_for_gold(fact: ConceptFact) -> set:
        return {fact.value}

    def response_for_pred(fact: ConceptFact) -> tuple:
        if fact is None:
            return (None, )
        if isinstance(fact.value, tuple):
            return fact.value
        return (fact.value, )  # None or single concept id

    gold_responses = []
    predicted_responses = []
    for gold_doc, pred_doc in zip(gold, predicted):
        if gold_doc.without_facts() != pred_doc.without_facts():
            raise ValueError("Predicted and gold sequences are not aligned")

        gold_facts = _group_facts(gold_doc)
        pred_facts = _group_facts(pred_doc)

        for key, gold_fact in gold_facts.items():  # mentions are aligned
            gold_responses.append(response_for_gold(gold_fact))
            predicted_responses.append(response_for_pred(pred_facts.get(key)))

    ret = {f"micro_recall@{k}": _compute_micro_recall_at_k(predicted_responses, gold_responses, k) for k in at_ks}
    ret["mean_reciprocal_rank"] = mean_reciprocal_rank(predicted_responses, gold_responses)
    ret["num_mentions"] = len(gold_responses)
    return ret
