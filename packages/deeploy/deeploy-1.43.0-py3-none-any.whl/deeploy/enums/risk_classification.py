from enum import Enum


class RiskClassification(Enum):
    """Class that contains the risk classification based on the EU AI Act"""

    UNCLASSIFIED = "unclassified"
    MINIMAL = "minimal"
    LIMITED = "limited"
    HIGH = "high"
    UNACCEPTABLE = "unacceptable"
