import logging
from ttex.log.handler import WandbHandler
import os
import shutil
from importlib.metadata import version
from typing import Dict, Optional
from wandb.sdk import launch


def test_wandb_handler(config: Optional[Dict] = None):
    # Update config
    ttex_version = version("tai_ttex")
    config_override = {"repo": "ttex", "version": ttex_version}

    # Iff there is a config, we are testing online
    if not config:
        prev_mode = os.environ.get("WANDB_MODE", "online")
        os.environ["WANDB_MODE"] = "offline"
        wandb_args = {
            "project": "ci-cd",
            "config": config_override,
        }
    else:
        config.update(config_override)
        # No project here because that is determined at launch
        wandb_args = {"config": config}

    handler = WandbHandler(wandb_args)
    logger = logging.getLogger("test_wandb_handler")
    logger.setLevel(logging.DEBUG)

    logger.addHandler(handler)
    logger.info("test")
    logger.info({"test": "test"})

    # Remove logging files
    shutil.rmtree(handler.run.dir)

    if not config:
        # Iff available, reset the mode
        os.environ["WANDB_MODE"] = prev_mode


if __name__ == "__main__":
    # This is to test launch from wandb
    if not os.environ.get("WANDB_CONFIG", None):
        raise RuntimeError("Needs to be launched from wandb")
    run_config = launch.load_wandb_config()
    test_wandb_handler(run_config)
