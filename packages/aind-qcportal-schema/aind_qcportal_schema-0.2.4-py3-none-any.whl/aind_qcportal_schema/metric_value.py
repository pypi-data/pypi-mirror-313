from pydantic import BaseModel, Field, model_validator
from typing import Any, Optional, Literal
from aind_data_schema.core.quality_control import Status


#  HOW TO USE
#  These objects should be attached to the QCMetric.value field. They affect how the
#  metric is rendered in the QC portal. The value field should be set to the value of the metric!


class DropdownMetric(BaseModel):
    """Dropdown metric schema

    The value field should either be "" or one of the options

    Renders as: https://panel.holoviz.org/reference/widgets/Select.html
    """

    value: Any = Field(..., title="Value")
    options: list[Any] = Field(..., title="Options")
    status: Optional[list[Status]] = Field(default=None, title="Option to status mapping")
    type: Literal["dropdown"] = "dropdown"
    status: Optional[list[Status]] = Field(
        default=None, title="Option to status mapping"
    )
    type: str = "dropdown"


class CheckboxMetric(BaseModel):
    """Checkbox metric schema

    The value field should either be "" or one or more of the options as a list

    Renders as: https://panel.holoviz.org/reference/widgets/Checkbox.html
    """

    value: Any = Field(..., title="Value")
    options: list[Any] = Field(..., title="Options")
    status: Optional[list[Status]] = Field(default=None, title="Option to status mapping")
    type: Literal["checkbox"] = "checkbox"


class RulebasedMetric(BaseModel):
    """Rulebased metric schema

    In general you should not be using this schema! This is a special metric that allows for a rule
     to be evaluated by the QC portal and the status to be set based on the result. The situation
     where you use this is if the value needs to be set by a user and the rule is fairly simple, e.g.
     the user sets the value to the number of visible cells, and the rule is "value>10". "value" *must*
     be included in the rule statement!

    If you are computing the status of an object yourself you should put the rule in the QCMetric.description field.
    """

    value: Any = Field(..., title="Value")
    rule: str = Field(
        ...,
        title="Runs eval(rule), Status.PASS when true, Status.FAIL when false",
    )


class MultiAssetMetric(BaseModel):
    """Multi-asset metric schema

    In general you should not be using this schema! This is a special
    metric that allows for a single metric to be evaluated across multiple assets.

    This should be used in combination with the QCEvaluation.evaluated_assets field.
    """

    values: list[Any] = Field(
        ...,
        title="Values",
        description="Length should match evaluated_assets. Use only basic types (str, int, float, bool)",
    )
    options: Optional[list[Any]] = Field(default=None, title="Options")
    type: Optional[str] = Field(
        default=None,
        title="Type",
        description="Set to 'dropdown' or 'checkbox' if you included options",
    )

    @model_validator(mode="after")
    def validate_type_if_options(cls, v):
        if v.options is not None and v.type is None:
            raise ValueError("Type must be set if options are included")

        return v
