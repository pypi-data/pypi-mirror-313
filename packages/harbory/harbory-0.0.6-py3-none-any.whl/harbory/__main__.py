import logging
import os

from harbory.commands import main

if os.environ.get("HARBORY_DEBUG"):
    LEVEL = logging.DEBUG
else:
    level_name = os.environ.get("HARBORY_LOG_LEVEL", "INFO")
    LEVEL = logging._nameToLevel.get(level_name, logging.INFO)

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", level=LEVEL)


def run() -> None:
    main(prog="harbory")


if __name__ == "__main__":
    run()
