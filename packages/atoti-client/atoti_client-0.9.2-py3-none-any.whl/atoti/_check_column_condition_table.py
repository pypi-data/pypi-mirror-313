from itertools import chain
from typing import Literal

from ._identification import ColumnIdentifier, TableIdentifier
from ._operation import (
    ComparisonCondition,
    Condition,
    ConditionCombinationOperatorBound,
    ConditionComparisonOperatorBound,
    ConditionTargetBound,
    IsinCondition,
    decombine_condition,
)


def check_column_condition_table(
    condition: Condition[
        ColumnIdentifier,
        ConditionComparisonOperatorBound,
        ConditionTargetBound,
        ConditionCombinationOperatorBound,
    ],
    /,
    *,
    attribute_name: Literal["subject", "target"],
    expected_table_identifier: TableIdentifier,
) -> None:
    error_message_template = f"Expected the {{attribute_name}} of the condition to belong to the table `{expected_table_identifier.table_name}` but got `{{table_name}}`."

    for decombined_conditions in decombine_condition(  # type: ignore[var-annotated]
        condition,
        allowed_subject_types=(ColumnIdentifier,),
    ):
        for sub_condition in chain(*decombined_conditions):
            assert isinstance(sub_condition, ComparisonCondition | IsinCondition)
            if attribute_name == "subject":
                if sub_condition.subject.table_identifier != expected_table_identifier:
                    raise ValueError(
                        error_message_template.format(
                            attribute_name=attribute_name,
                            table_name=sub_condition.subject.table_identifier.table_name,
                        ),
                    )
            elif attribute_name == "target":
                assert isinstance(sub_condition, ComparisonCondition)
                assert isinstance(sub_condition.target, ColumnIdentifier)
                if sub_condition.target.table_identifier != expected_table_identifier:
                    raise ValueError(
                        error_message_template.format(
                            attribute_name=attribute_name,
                            table_name=sub_condition.target.table_identifier.table_name,
                        ),
                    )
