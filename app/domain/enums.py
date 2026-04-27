from enum import Enum

class TicketCategory(str, Enum):
    TECHNICAL = "technical"
    BILLING = "billing"
    FEATURE_REQUEST = "feature_request"
    SPAM = "spam"

class UrgencyLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ProcessingStatus(str, Enum):
    SUCCESS = "success"
    FLAGGED = "flagged" # Used if the AI detects dangerous or spam content
    FAILED = "failed"