from dataclasses import dataclass
from functools import partial
from itertools import chain, zip_longest
from typing import Iterable, Iterator, Union

from tdm import TalismanDocument
from tdm.abstract.datamodel import AbstractDomainType
from tdm.datamodel.facts import AtomValueFact, ConceptFact, PropertyFact, RelationFact
from typing_extensions import Self

from talisman_tools.commands.model.commands.evaluate.evaluation import _evaluate
from talisman_tools.commands.model.commands.evaluate.helpers import get_original_type_id
from tp_interfaces.helpers.datamodel.domain import get_id

NERFact = Union[ConceptFact, AtomValueFact]
LinkFact = Union[RelationFact, PropertyFact]


@dataclass(frozen=True, slots=True)
class RelationTupleView:
    """"
    A utility class that represents relation facts as dataclasses (without fact ids)
    """

    type_id: str | AbstractDomainType
    source: NERFact
    target: NERFact

    def __post_init__(self):
        """
        Replace domain type id of relation with the original one.
        """
        object.__setattr__(self, 'type_id', get_original_type_id(get_id(self.type_id)))

    @classmethod
    def from_fact(cls, fact: RelationFact) -> Self:
        return RelationTupleView(fact.type_id, fact.source, fact.target)

    @classmethod
    def from_doc(cls, doc: TalismanDocument, excluded_types: dict) -> Iterator[Self]:
        relation_blacklist = set(excluded_types.get('relations', []))

        for fact in doc.get_facts(LinkFact):
            if get_original_type_id(get_id(fact.type_id)) not in relation_blacklist:
                yield cls.from_fact(fact)


def _fact_type(query, fact: RelationTupleView) -> str:
    return fact.type_id


def _source_target_types(query, link_fact: RelationTupleView) -> tuple[str, str]:
    return get_id(link_fact.source.type_id), get_id(link_fact.target.type_id)


def _link_signature(query, link_fact: RelationTupleView) -> tuple[str, str, str]:
    return get_id(link_fact.source.type_id), get_id(link_fact.target.type_id), link_fact.type_id


_LINK_CATEGORIZERS = {
    "fact_type": _fact_type,
    "source_target_types": _source_target_types,
    "signature": _link_signature
}


def evaluate_relext(predicted: Iterable[TalismanDocument], gold: Iterable[TalismanDocument], eval_config: dict) -> dict[str, dict]:
    return _evaluate(
        predicted, gold, partial(RelationTupleView.from_doc, excluded_types=eval_config.get('excluded_types', {})), _LINK_CATEGORIZERS
    )


def evaluate_relext_upper_bound(
    predicted: Iterable[TalismanDocument],
    gold: Iterable[TalismanDocument],
    eval_config: dict
) -> dict[str, dict]:
    predicted, gold = tuple(predicted), tuple(gold)
    predicted_w_gold_rels = []

    for pred_doc, gold_doc in zip_longest(predicted, gold):
        if pred_doc is None or gold_doc is None:
            raise ValueError("Predicted and gold documents iterables length mismatch")

        pred_entity_facts = set(pred_doc.get_facts(NERFact))
        gold_entity_facts = set(gold_doc.get_facts(NERFact)).intersection(pred_entity_facts)

        def filter_(fact: RelationFact) -> bool:
            return fact.source in gold_entity_facts and fact.target in gold_entity_facts

        possible_to_find_gold_rels = gold_doc.get_facts(RelationFact, filter_=filter_)

        predicted_w_gold_rels.append(
            gold_doc.without_facts(gold_doc.get_facts()).with_facts(chain(gold_entity_facts, possible_to_find_gold_rels))
        )

    return evaluate_relext(predicted_w_gold_rels, gold, eval_config)
