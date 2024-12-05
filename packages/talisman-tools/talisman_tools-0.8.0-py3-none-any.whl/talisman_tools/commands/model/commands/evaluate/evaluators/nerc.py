from dataclasses import dataclass
from functools import partial
from typing import Iterable, Iterator

from tdm import TalismanDocument
from tdm.datamodel.facts import MentionFact
from tdm.datamodel.mentions import TextNodeMention
from typing_extensions import Self

from talisman_tools.commands.model.commands.evaluate.evaluation import _evaluate
from tp_interfaces.helpers.datamodel.domain import get_id


@dataclass(frozen=True, slots=True)
class MentionTupleView:
    """"
    A utility class that represents mention facts as named tuples (without fact ids)
    """

    type_id: str

    node_id: str
    start: int
    end: int

    @classmethod
    def from_fact(cls, fact: MentionFact) -> Self:
        if not isinstance(fact.mention, TextNodeMention):
            raise ValueError(f'Cannot create {cls.__class__.__name__} from fact with mention of class {fact.mention.__class__.__name__}!')
        return cls(get_id(fact.value.type_id), fact.mention.node_id, fact.mention.start, fact.mention.end)

    @classmethod
    def from_doc(cls, doc: TalismanDocument, excluded_types: dict) -> Iterator[Self]:
        values_blacklist = set(excluded_types.get('values', []))

        for fact in doc.get_facts(MentionFact, filter_=lambda m: isinstance(m.mention, TextNodeMention)):
            if get_id(fact.value.type_id) not in values_blacklist:
                yield cls.from_fact(fact)


def _fact_type(query, fact: MentionTupleView) -> str:
    return fact.type_id


_NERC_CATEGORIZERS = {
    'fact_type': _fact_type
}


def evaluate_nerc(predicted: Iterable[TalismanDocument], gold: Iterable[TalismanDocument], eval_config: dict) -> dict[str, dict]:
    return _evaluate(
        predicted, gold, partial(MentionTupleView.from_doc, excluded_types=eval_config.get('excluded_types', {})), _NERC_CATEGORIZERS
    )
