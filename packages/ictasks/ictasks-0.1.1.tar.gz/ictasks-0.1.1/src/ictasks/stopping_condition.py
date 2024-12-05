"""
This module has stopping conditions for tasks
"""

from pathlib import Path
import os
import logging

from pydantic import BaseModel

from iccore.filesystem import file_contains_string

logger = logging.getLogger(__name__)


class StoppingCondition(BaseModel):
    """
    This condition stops processing if a particular file
    is found with a predefined phrase.
    """

    stopmagic: str = ""
    stopfile: Path | None = None

    def check_magic(self, path: Path) -> bool:
        """
        Is the magic phrase found in the file?
        """
        return file_contains_string(path, self.stopmagic)

    def eval(self, path: Path) -> bool:
        """
        Stop processing if the stop condition is hit
        """
        if not self.stopfile:
            return False

        stopfile_path = path / self.stopfile

        if os.path.exists(stopfile_path) and self.stopmagic == "":
            logger.info("Stop-file %s is present.", stopfile_path)
            return True

        if os.path.exists(stopfile_path) and self.check_magic(stopfile_path):
            logger.info("Stop file %s contains magic %s", stopfile_path, self.stopmagic)
            return True
        return False
