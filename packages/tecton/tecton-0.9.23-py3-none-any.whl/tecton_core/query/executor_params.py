from enum import Enum


class QueryTreeStep(Enum):
    """Query trees are composed of steps.

    Each step may have its own compute, and may stage its results in preparation for the next step.

    Query trees do not have to have all steps. For example, a materialization query tree for a batch feature view will
    not have any nodes in the ODFV step.
    """

    # Runs data source scans.
    DATA_SOURCE = 1
    # Runs feature view transformations to produce un-aggregated feature data.
    PIPELINE = 2
    # Runs model inference (only used by text embeddings right now).
    MODEL_INFERENCE = 3
    # Runs partial aggregations, full aggregations, and the as-of join.
    AGGREGATION = 4
    # Runs on-demand transformations.
    ODFV = 5
