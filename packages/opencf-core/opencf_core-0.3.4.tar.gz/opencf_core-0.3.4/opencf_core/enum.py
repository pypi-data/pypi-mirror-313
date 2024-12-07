"""
Dependencies:

- aenum.Enum: For creating the FileType enumeration.
"""

from typing import TYPE_CHECKING, Callable, Type

from aenum import extend_enum  # type: ignore # pylint: disable=import-error

from .logging_config import logger

if TYPE_CHECKING:
    # this is only processed by MyPy (i.e. not at runtime)
    from enum import Enum
else:
    # this is real runtime code
    from aenum import Enum


def extend_enum_with_methods(
    inherited_enum: Type[Enum],
    added_enum: Type[Enum],
    filter_func: Callable[[Enum], bool],
) -> None:
    """
    Extends an Enum class with members and methods from another Enum class based on a filter function.

    This function takes three arguments: `inherited_enum`, `added_enum`, and `filter_func`. It adds all the members from
    `added_enum` to `inherited_enum` that pass the filter function provided. It also copies all the methods (including
    class methods) from both `inherited_enum` and `added_enum` to the extended `inherited_enum` class.

    Args:
        inherited_enum (Type[Enum]): The Enum class to be extended with new members and methods.
        added_enum (Type[Enum]): The Enum class whose members and methods will be added to `inherited_enum`.
        filter_func (Callable[[Enum], bool]): A function that filters which members to add from `added_enum` to `inherited_enum`.

    Returns:
        None
    """

    # Add new members from added_enum to inherited_enum based on the filter function
    for name, member in added_enum.__members__.items():
        if filter_func(member):
            extend_enum(inherited_enum, name, member.value)
        else:
            logger.warning(
                "Member '%s' from %s did not pass the filter function.",
                name,
                added_enum.__name__,
            )

    # Copy methods from inherited_enum and added_enum to the new class
    for method_name, method in {
        **added_enum.__dict__,
        **inherited_enum.__dict__,
    }.items():
        if callable(method) or isinstance(method, classmethod):
            setattr(inherited_enum, method_name, method)
