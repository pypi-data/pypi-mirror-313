import time
from functools import partial
from itertools import chain
from pathlib import Path
from typing import Optional

from tdm import TalismanDocument
from tdm.datamodel.domain import Domain
from tdm.datamodel.facts import AtomValueFact, ConceptFact, MentionFact, PropertyFact

from talisman_tools.commands.model.commands.evaluate.evaluators import evaluators
from talisman_tools.commands.model.commands.evaluate.helpers import build_domain, filter_facts, print_scores, replace_with_domain
from talisman_tools.configure.configure import read_config
from talisman_tools.plugin import DomainPlugins
from tp_interfaces.abstract import AbstractDocumentProcessor
from tp_interfaces.domain.manager import DomainManager
from tp_interfaces.readers.abstract import AbstractReader


def keep_nerc(doc: TalismanDocument) -> TalismanDocument:

    facts = chain(
        doc.get_facts(ConceptFact),
        doc.get_facts(AtomValueFact),
        doc.get_facts(MentionFact),
        doc.get_facts(PropertyFact)
    )
    return doc.without_facts(doc.get_facts()).with_facts(facts)


def clear_values(doc: TalismanDocument) -> TalismanDocument:
    return doc.with_facts(
        map(lambda f: f.with_changes(value=tuple()), doc.get_facts(ConceptFact)),  # TODO: replace value with None instead of empty tuple
    )


def clear_chains(doc: TalismanDocument) -> TalismanDocument:
    pass


mode = {
    'all': lambda doc: doc.without_facts(doc.get_facts()),  # start from clear document (no facts provided)
    'nerc': lambda doc: doc.without_facts(doc.get_facts()),  # start from clear document (no facts provided)
    'relext': keep_nerc,  # start from document with concept, value, mention and property facts (no link facts, no fact values)
    'dmb': clear_values,  # start from document with facts without values
    'coref': clear_chains
}


async def evaluate(
        processor: AbstractDocumentProcessor,
        eval_mode: str,
        reader: AbstractReader,
        config_path: Path,
        eval_config_path: Path,
        input_reader: Optional[AbstractReader] = None
):
    """
    Core function that evaluates a document processor under the given task.
    """

    # load gold documents
    gold_docs = tuple(reader.read())

    # build domain based on the gold documents
    domain: Domain = build_domain(gold_docs)
    DomainManager().set_producer(DomainPlugins.plugins[None]()(domain))  # DMBCommonnessStub

    # replace old type_id of fact with domain types
    replace_with_domain_ = partial(replace_with_domain, domain=domain)
    gold_docs = tuple(map(replace_with_domain_, gold_docs))

    # load raw documents (to be processed)
    actual_docs = tuple(map(mode[eval_mode], gold_docs)) if input_reader is None else tuple(map(replace_with_domain_, input_reader.read()))

    # process raw documents
    async with DomainManager() and processor:

        evaluation_start = time.time()

        processor_config_type = processor.config_type
        config = processor_config_type.parse_obj(read_config(config_path)) if config_path else processor_config_type()
        actual_docs = await processor.process_docs(actual_docs, config)

        evaluation_end = time.time()

    # evaluate result
    filtered_docs = [filter_facts(doc, domain) for doc in actual_docs]
    eval_config = read_config(eval_config_path) if eval_config_path else {}
    scores = {name: evaluator(filtered_docs, gold_docs, eval_config.get(name, {})) for name, evaluator in evaluators[eval_mode].items()}

    print_scores(scores)
    print(f'Total evaluation time: {evaluation_end - evaluation_start:.04f} seconds')
