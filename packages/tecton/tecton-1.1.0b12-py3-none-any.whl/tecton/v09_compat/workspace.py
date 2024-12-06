import logging
from enum import Enum


logger = logging.getLogger(__name__)


class ValidationMode(str, Enum):
    EXPLICIT = "explicit"
    AUTOMATIC = "auto"
    SKIP = "skip"


def set_validation_mode(mode: ValidationMode):
    """Deprecated"""
    logger.warning(
        "The set_validation_mode() method is deprecated and will be removed in a future version. As of "
        "Tecton version 1.0, objects are automatically validated on creation"
    )
