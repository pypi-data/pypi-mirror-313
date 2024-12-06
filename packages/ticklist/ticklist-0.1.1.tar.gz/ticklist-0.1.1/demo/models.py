from enum import Enum
from typing import Annotated

from pydantic import BaseModel, ConfigDict

from ticklist import tick_annotations as ta


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Colors(Enum):
    BLUE = "blue"
    RED = "red"
    GREEN = "green"


class InteriorColor(Enum):
    GREY = "grey"
    BLACK = "black"


class Engine(Enum):
    FOUR_CILINDER = "four_cilinder"
    SIX_CILINDER = "six_cilinder"


class Normal(StrictModel):
    interior_color: InteriorColor


class Sports(StrictModel):
    interior_color: InteriorColor
    engine: Engine = Engine.FOUR_CILINDER


class MyCar(StrictModel):
    customer_name: str

    color: Colors

    edition: (
        Annotated[Normal, ta.Label("normal")] | Annotated[Sports, ta.Label("sports")]
    )

    extra_insurance: Annotated[
        bool, ta.BooleanLabels(label_for_false="no", label_for_true="yes")
    ] = True
