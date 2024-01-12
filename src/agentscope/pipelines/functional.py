# -*- coding: utf-8 -*-
""" Functional counterpart for Pipeline """

from typing import Callable, Sequence, Optional
from typing import Any
from typing import Mapping
from ..agents import _Operator


def placeholder(x: dict = None) -> dict:
    r"""A placeholder that do nothing.

    Acts as a placeholder in branches that do not require any operations in
    flow control like if-else/switch
    """
    return x


def sequentialpipeline(
    operators: Sequence[_Operator],
    x: Optional[dict] = None,
) -> dict:
    """Functional version of SequentialPipeline.

    Args:
        operators (`Sequence[Operator]`):
            Participating operators.
        x (`Optional[dict]`, defaults to `None`):
            The input dictionary.

    Returns:
        `dict`: the output dictionary.
    """
    if len(operators) == 0:
        raise ValueError("No operators provided.")

    msg = operators[0](x)
    for operator in operators[1:]:
        msg = operator(msg)
    return msg


def ifelsepipeline(
    x: dict,
    condition_func: Callable,
    if_body_operator: _Operator,
    else_body_operator: _Operator = placeholder,
) -> dict:
    """Functional version of IfElsePipeline.

    Args:
        x (`dict`):
            The input dictionary.
        condition_func (`Callable`):
            A function that determines whether to exeucte `if_body_operator`
            or `else_body_operator` based on x.
        if_body_operator (`_Operator`):
            An operator executed when `condition_func` returns True.
        else_body_operator (`_Operator`, defaults to `placeholder`):
            An operator executed when condition_func returns False,
            does nothing and just return the input by default.

    Returns:
        `dict`: the output dictionary.
    """
    if condition_func(x):
        return if_body_operator(x)
    else:
        return else_body_operator(x)


def switchpipeline(
    x: dict,
    condition_func: Callable[[dict], Any],
    case_operators: Mapping[Any, _Operator],
    default_operator: _Operator = placeholder,
) -> dict:
    """Functional version of SwitchPipeline.


    Args:
        x (`dict`):
            The input dictionary.
        condition_func (`Callable[[dict], Any]`):
            A function that determines which case_operator to execute based
            on the input x.
        case_operators (`Mapping[Any, _Operator]`):
            A dictionary containing multiple operators and their
            corresponding trigger conditions.
        default_operator (`_Operator`, defaults to `placeholder`):
            An operator that is executed when the actual condition do not
            meet any of the case_operators, does nothing and just return the
            input by default.

    Returns:
        dict: the output dictionary.
    """
    target_case = condition_func(x)
    if target_case in case_operators:
        return case_operators[target_case](x)
    else:
        return default_operator(x)


def forlooppipeline(
    x: dict,
    loop_body_operator: _Operator,
    max_loop: int,
    break_func: Callable[[dict], bool] = lambda _: False,
) -> dict:
    """Functional version of ForLoopPipeline.

    Args:
        x (`dict`):
            The input dictionary.
        loop_body_operator (`_Operator`):
            An operator executed as the body of the loop.
        max_loop (`int`):
            maximum number of loop executions.
        break_func (`Callable[[dict], bool]`):
            A function used to determine whether to break out of the loop
            based on the output of the loop_body_operator, defaults to
            `lambda _: False`

    Returns:
        `dict`: The output dictionary.
    """
    for _ in range(max_loop):
        # loop body
        x = loop_body_operator(x)
        # check condition
        if break_func(x):
            break
    return x


def whilelooppipeline(
    x: dict,
    loop_body_operator: _Operator,
    condition_func: Callable[[int, dict], bool] = lambda _, __: False,
) -> dict:
    """Functional version of WhileLoopPipeline.

    Args:
        x (`dict`): The input dictionary.
        loop_body_operator (`_Operator`): An operator executed as the body of
            the loop.
        condition_func (`Callable[[int, dict], bool]`, optional): A function
            that determines whether to continue executing the loop body based
            on the current loop number and output of the loop_body_operator,
            defaults to `lambda _,__: False`

    Returns:
        `dict`: the output dictionary.
    """
    i = 0
    while condition_func(i, x):
        # loop body
        x = loop_body_operator(x)
        # check condition
        i += 1
    return x