import argparse
import json
from logging import getLogger
from pathlib import Path

from harbory.constants import DEFAULT_HARBORY_SETTINGS_PATH
from harbory.machinery import (
    MachineryEvaluationSettings,
    MachineryPredictionSettings,
    MachineryTraningSettings,
    evaluate,
    predict,
    train,
)
from harbory.settings import HarborySettings

from .subcommand import Subcommand

logger = getLogger(__name__)


@Subcommand.register("machinery")
class MachineryCommand(Subcommand):
    def setup(self) -> None:
        self.parser.add_argument(
            "--settings",
            type=Path,
            default=DEFAULT_HARBORY_SETTINGS_PATH,
            help="settings file path",
        )


@MachineryCommand.register("train")
class MachineryTrainCommand(MachineryCommand):
    def setup(self) -> None:
        self.parser.add_argument("config", type=str, help="config file path")
        self.parser.add_argument("archive", type=str, help="archive file path")
        self.parser.add_argument("--overrides", type=str, default=None, help="overrides jsonnet file path")

    def run(self, args: argparse.Namespace) -> None:
        logger.info(f"Loading harbory settings from {args.settings}...")
        _ = HarborySettings.from_file(args.settings)

        logger.info(f"Loading settings from {args.config}...")
        settings = MachineryTraningSettings.from_jsonnet(  # type: ignore[var-annotated]
            args.config, overrides=args.overrides
        )

        logger.info("Start training...")
        archive = train(
            model=settings.model,
            train_dataset=settings.train_dataset,
            valid_dataset=settings.valid_dataset,
            test_dataset=settings.test_dataset,
            setup=settings.setup,
            evaluation=settings.evaluation,
            preprocessor=settings.preprocessor,
        )

        logger.info(f"Save archive to {args.archive}...")
        archive.save(args.archive)

        logger.info("Training completed.")


@MachineryCommand.register("predict")
class MachineryPredictCommand(MachineryCommand):
    def setup(self) -> None:
        self.parser.add_argument("config", type=str, help="config file path")
        # self.parser.add_argument("archive", type=str, help="archive file path")
        self.parser.add_argument("--overrides", type=str, default=None, help="overrides jsonnet file path")

    def run(self, args: argparse.Namespace) -> None:
        logger.info(f"Loading harbory settings from {args.settings}...")
        _ = HarborySettings.from_file(args.settings)

        logger.info(f"Loading training settings from {args.config}...")
        settings = MachineryPredictionSettings.from_jsonnet(  # type: ignore[var-annotated]
            args.config,
            overrides=args.overrides,
        )

        predictions = predict(
            model=settings.model,
            dataset=settings.dataset,
            setup=settings.setup,
            params=settings.params,
            preprocessor=settings.preprocessor,
            postprocessor=settings.postprocessor,
            batch_size=settings.batch_size,
            max_workers=settings.max_workers,
        )

        settings.output.save(predictions)


@MachineryCommand.register("evaluate")
class MachineryEvaluateCommand(MachineryCommand):
    def setup(self) -> None:
        self.parser.add_argument("config", type=str, help="config file path")
        self.parser.add_argument("--overrides", type=str, default=None, help="overrides jsonnet file path")

    def run(self, args: argparse.Namespace) -> None:
        logger.info(f"Loading harbory settings from {args.settings}...")
        _ = HarborySettings.from_file(args.settings)

        logger.info(f"Loading training settings from {args.config}...")
        settings = MachineryEvaluationSettings.from_jsonnet(  # type: ignore[var-annotated]
            args.config,
            overrides=args.overrides,
        )

        metrics = evaluate(
            model=settings.model,
            dataset=settings.dataset,
            setup=settings.setup,
            preprocessor=settings.preprocessor,
        )

        print(json.dumps(metrics, indent=2, ensure_ascii=False))
