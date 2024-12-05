from argparse import Namespace

from talisman_tools.configure.configure import read_config
from tp_interfaces.abstract import AbstractDocumentProcessor
from tp_interfaces.readers.abstract import AbstractReader


async def async_action(processor: AbstractDocumentProcessor, serializer, reader: AbstractReader, args: Namespace):

    async with processor:
        processor_config_type = processor.config_type
        config = processor_config_type.parse_obj(read_config(args.config)) if args.config else processor_config_type()
        serializer(processor.process_stream(reader.read(), config, args.batch))
