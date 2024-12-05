import logging
from argparse import Namespace
from pathlib import Path

from talisman_tools.configure import read_config
from talisman_tools.plugin import TrainerPlugins
from tp_interfaces.abstract import AbstractTrainer
from tp_interfaces.abstract.processor.trainer import DEFAULT_CACHE_DIR

logger = logging.getLogger(__name__)


def train(args: Namespace):
    config = read_config(args.config_path)
    trainer_plugin = config['plugin']
    trainer_model = config['model']
    trainer_config = config['config']
    if 'evaluation_strategy' in trainer_config.get('trainer', {}) and not trainer_config['trainer']['evaluation_strategy']:
        trainer_config['trainer']['evaluation_strategy'] = 'no'
    trainer: AbstractTrainer = TrainerPlugins.plugins[trainer_plugin][trainer_model].from_config(trainer_config)

    cache_dir = Path(args.cache_dir) if args.cache_dir is not None else DEFAULT_CACHE_DIR
    if args.ignore_cache:
        cache_dir = None

    train_results = trainer.train(cache_dir)
    train_results.model.save(Path(args.trained_model_path))
