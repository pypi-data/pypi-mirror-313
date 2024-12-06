import logging
import wandb
import ast
from wandb.sdk.wandb_run import Run


class WandbHandler(logging.Handler):
    """
    Handler that will emit results to wandb
    """

    def __init__(self, wandb_run: Run, level=logging.NOTSET):
        super().__init__(level)
        self.run = wandb_run

    def emit(self, record):
        msg = record.getMessage()
        try:
            msg_dict = ast.literal_eval(msg)
            assert isinstance(msg_dict, dict)
            wandb.log(msg_dict)
        except ValueError:
            pass
