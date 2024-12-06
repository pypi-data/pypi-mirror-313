from typing import Annotated

from pydantic import Field

StrictlyPositiveNumber = Annotated[int | float, Field(gt=0)]
