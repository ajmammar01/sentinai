from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Union, Literal
from .enums import TicketCategory, UrgencyLevel, ProcessingStatus

class ExtractedTicket(BaseModel):
    """The schema for a successfully processed support ticket."""
    type: Literal["ticket"] = "ticket"
    sender_email: EmailStr
    sender_name: Optional[str] = Field(description="The full name of the sender, if provided") # NEW FIELD
    subject: str
    category: TicketCategory
    urgency: UrgencyLevel
    summary: str = Field(description="A 1-sentence summary of the user's request")
    items_to_action: list[str] = Field(description="List of specific tasks mentioned in the email")

class FlaggedContent(BaseModel):
    """The schema for emails that are spam, toxic, or irrelevant."""
    type: Literal["flagged"] = "flagged"
    reason: str = Field(description="Reason why this content was flagged (e.g., spam, offensive)")

# This is the "Discriminated Union"
# It tells the AI: You MUST return either an ExtractedTicket OR FlaggedContent
ProcessedResult = Union[ExtractedTicket, FlaggedContent]

class ProcessingResponse(BaseModel):
    """The final wrapper for our AI's output."""
    status: ProcessingStatus
    data: ProcessedResult