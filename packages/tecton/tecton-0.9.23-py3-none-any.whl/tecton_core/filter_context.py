from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class FilterContext:
    """
    ``FilterContext`` is passed as an argument to Data Source Function for time filtering.
    """

    start_time: Optional[datetime]
    end_time: Optional[datetime]
