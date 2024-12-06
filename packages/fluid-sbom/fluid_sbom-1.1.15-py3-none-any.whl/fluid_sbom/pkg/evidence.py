from enum import (
    Enum,
)


class Evidence(Enum):
    EVIDENCE_ANNOTATION_KEY = "evidence"
    PRIMARY_EVIDENCE_ANNOTATION = "primary"
    SUPPORTING_EVIDENCE_ANNOTATION = "supporting"
