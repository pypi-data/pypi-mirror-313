from typing import Literal

from ..base_settings import BaseModelSettings


class TCallModelSettings(BaseModelSettings):
    """
    Change these settings to tweak the model's behavior.

    Base on https://platform.openai.com/docs/api-reference/chat/create
    """

    max_iterations: int = 10  # Maximum back and fourth allowed
    tool_choice: Literal["auto", "required"] = "auto"
