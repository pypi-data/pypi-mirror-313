from typing import Optional

from pydantic import BaseModel


class CreateGreetingV0(BaseModel):
    greeting_is_anonymous: bool
    greeting_anonymous_sender_name: Optional[str] = None
    greeting_text: Optional[str] = None
