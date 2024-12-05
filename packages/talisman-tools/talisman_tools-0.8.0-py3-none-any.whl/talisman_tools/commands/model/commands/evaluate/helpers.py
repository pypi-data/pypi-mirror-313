import json
from dataclasses import replace
from itertools import chain
from typing import TypeVar, Union

from more_itertools.more import always_iterable
from tdm import TalismanDocument
from tdm.abstract.datamodel import AbstractDomainType, AbstractFact, AbstractLinkFact, AbstractValue
from tdm.datamodel.domain import Domain
from tdm.datamodel.facts import AtomValueFact, ConceptFact, MentionFact, PropertyFact, RelationFact

from tp_interfaces.domain.abstract import RelExtModel
from tp_interfaces.domain.model.types import AtomValueType, ConceptType, IdentifyingPropertyType, PropertyType, RelationType
from tp_interfaces.helpers.datamodel.domain import get_id

DELIMITER = '::'


def unique_relation_type_id(type_id: str, source_type_id: str, target_type_id: str):
    """
    In some datasets (e.g. DocRED) relations can be between different sets of source and target entity types. To meet requirements of
    domain we construct unique relation type ids for them (e.g. rel.type_id=f'{rel.type_id}::{source.type_id}_{target.type_id}').
    """
    return (type_id + DELIMITER + source_type_id + '_' + target_type_id).replace(' ', '_')


def get_original_type_id(type_id: str):
    """
    In some datasets (e.g. DocRED) relations can be between different sets of source and target entity types. To meet requirements of
    domain we construct unique relation type ids for them (e.g. rel.type_id=f'{rel.type_id}::{source.type_id}_{target.type_id}').
    This function returns original relation type id.
    """
    return type_id.split(DELIMITER)[0]


def print_scores(scores: dict[str, dict]):
    def round_floats(val, precision=4):
        if isinstance(val, int):
            return val
        if isinstance(val, float):
            return round(val, precision)
        if isinstance(val, dict):
            return {k: round_floats(v) for k, v in val.items()}
        raise ValueError

    def stringify_keys(d: dict):
        ret = {}
        for key, val in d.items():
            if isinstance(key, (tuple, frozenset)):
                key = str(key)
            if isinstance(val, dict):
                val = stringify_keys(val)

            ret[key] = val

        return ret

    json_repr = json.dumps(stringify_keys(round_floats(scores)), sort_keys=True, indent=2)
    print(json_repr)


_Value = TypeVar('_Value', bound=AbstractValue)


def _get_value_type(value_fact: AtomValueFact) -> _Value:
    value_types = list({v.__class__ for v in always_iterable(value_fact.value)})
    if len(value_types) != 1 or not isinstance(value_types[0], AbstractValue):
        return AbstractValue

    return value_types[0]


def get_domain_type(fact: AbstractFact, pretrained_types: dict[str, str] | None = None,
                    nerc_pretrained: bool = True, type_names: dict[str, str] = None) -> AbstractDomainType:
    """
    Returns fact's domain type (or build fake one).
    NOTE: each type must have a unique id.
    """

    if hasattr(fact, 'type_id') and isinstance(fact.type_id, AbstractDomainType):
        return fact.type_id

    pretrained = pretrained_types.get(fact.type_id) if hasattr(fact, 'type_id') else None
    type_name = type_names.get(fact.type_id) if hasattr(fact, 'type_id') and type_names else None

    if isinstance(fact, ConceptFact):
        return ConceptType(id=fact.type_id, name=type_name)
    if isinstance(fact, AtomValueFact):
        value_type = _get_value_type(fact)
        return AtomValueType(fact.type_id, value_type, id=fact.type_id, pretrained_nerc_models=(pretrained,) if pretrained else ())
    if isinstance(fact, MentionFact):
        return get_domain_type(fact.value, pretrained_types=pretrained_types, nerc_pretrained=nerc_pretrained, type_names=type_names)

    if not isinstance(fact, AbstractLinkFact):
        raise ValueError

    source_type = get_domain_type(fact.source, pretrained_types=pretrained_types, nerc_pretrained=nerc_pretrained, type_names=type_names)
    target_type = get_domain_type(fact.target, pretrained_types=pretrained_types, nerc_pretrained=nerc_pretrained, type_names=type_names)

    # Now fact is property fact or relation fact
    # In some datasets (e.g. DocRED) relations can be between different sets of source and target entity types.
    # To meet requirements of domain we construct unique relation type ids for them
    params = {
        'name': type_name,
        'source': source_type,
        'target': target_type,
        'id': unique_relation_type_id(fact.type_id, get_id(source_type), get_id(target_type))
    }

    if isinstance(fact, PropertyFact) and nerc_pretrained:
        params['pretrained_nerc_models'] = (pretrained,) if pretrained else ()
        return IdentifyingPropertyType(**params, isIdentifying=True)

    params['pretrained_relext_models'] = (RelExtModel(relation_type=pretrained),) if pretrained else ()

    if isinstance(fact, PropertyFact):
        return PropertyType(**params, isIdentifying=False)
    if isinstance(fact, RelationFact):
        return RelationType(**params)
    raise ValueError


def build_domain(gold_docs: tuple[TalismanDocument, ...], pretrained_types: dict[str, str] | None = None, nerc_pretrained: bool = True,
                 type_names: dict[str, str] | None = None) -> Domain:
    """
    Builds domain based on the facts from gold documents.
    In the case if type_id of some fact is string, fake AbstractDomainType is created, otherwise original type_id is used.
    """
    return Domain(
        get_domain_type(fact, pretrained_types, nerc_pretrained, type_names) for fact in chain.from_iterable(
            doc.get_facts() for doc in gold_docs
        )
    )


def replace_with_domain(doc: TalismanDocument, domain: Domain, pretrained_types: dict[str, str] | None = None,
                        nerc_pretrained: bool = True, type_names: dict[str, str] | None = None):
    """
    Creates a new facts with domain type instead of its identifier.
    """

    def _replace_with_domain(fact: AbstractFact):
        if isinstance(fact, Union[PropertyFact | RelationFact]):
            fact = replace(fact, type_id=get_domain_type(fact, pretrained_types, nerc_pretrained, type_names))
        return fact.replace_with_domain(domain)

    facts = map(_replace_with_domain, doc.get_facts())
    return doc.without_facts(doc.get_facts()).with_facts(facts=facts, update=True)


def filter_facts(doc: TalismanDocument, domain: Domain):
    """
    Drops facts from document that are not represented in the domain.
    """

    def _filter_facts(fact: AbstractFact):
        try:
            if hasattr(fact, 'type_id'):
                domain.get_type(get_id(fact.type_id))
        except KeyError:
            return False
        return True

    facts = doc.get_facts(filter_=_filter_facts)
    return doc.without_facts(doc.get_facts()).with_facts(facts, update=True)
