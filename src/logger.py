"""
=========================================================
Gesture Controls
Logger Module

Author : Ishant Garg
Version : 1.0.0
=========================================================
"""

import logging
from pathlib import Path
from datetime import datetime


class AppLogger:

    def __init__(self):

        self.log_directory = Path("logs")
        self.log_directory.mkdir(
            exist_ok=True
        )

        filename = datetime.now().strftime(
            "GestureControls_%Y%m%d_%H%M%S.log"
        )

        logfile = self.log_directory / filename

        logging.basicConfig(
            filename=logfile,
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s"
        )

        self.logger = logging.getLogger("GestureControls")

    # --------------------------------------------------

    def startup(self):

        self.logger.info(
            "Application Started"
        )

    # --------------------------------------------------

    def shutdown(self):

        self.logger.info(
            "Application Closed"
        )

    # --------------------------------------------------

    def gesture(self, gesture):

        self.logger.info(
            f"Gesture : {gesture}"
        )

    # --------------------------------------------------

    def action(self, action):

        self.logger.info(
            f"Action : {action}"
        )

    # --------------------------------------------------

    def info(self, message):

        self.logger.info(message)

    # --------------------------------------------------

    def warning(self, message):

        self.logger.warning(message)

    # --------------------------------------------------

    def error(self, message):

        self.logger.error(message)

    # --------------------------------------------------

    def exception(self, error):

        self.logger.exception(error)
        