from functools import reduce
from click import ClickException, echo
from click._compat import get_text_stderr
import typing as t
from gettext import gettext as _


##################################
# Define messages for exceptions #
##################################

ONLY_ADD_OR_REMOVE = "Only one of --add or --remove can be specified."
MUST_HAVE_ADD_OR_REMOVE = "One of --add or --remove must be specified."
OVERWRITE_ONLY_WHEN_ADDING = (
    "--overwrite can only be specified when adding authentication."
)


def _format_message(exception):
    if hasattr(exception, "format_message"):
        return exception.format_message()
    else:
        return str(exception)


def _build_message(exception):
    msg = _format_message(exception)

    while exception.__cause__:
        msg += f"\n{_format_message(exception.__cause__)}"
        exception = exception.__cause__

    return msg


class BasePloomberCloudException(ClickException):
    """Base exception for all Ploomber Cloud exceptions"""

    def __init__(self, message):
        super().__init__(message)
        # this attribute will allow the @modify_exceptions decorator to add the
        # community link
        self.modify_exception = True

    def get_message(self):
        return f"Error: {_build_message(self)}"

    def show(self, file: t.Optional[t.IO] = None) -> None:
        if file is None:
            file = get_text_stderr()
            echo(_(self.get_message()), file=file)
        else:
            print(_(self.get_message()))


class InvalidPloomberConfigException(BasePloomberCloudException):
    """Exception for invalid ploomber-config.json"""

    pass


class PloomberCloudRuntimeException(BasePloomberCloudException):
    """Exception for Ploomber Cloud runtime exceptions"""

    pass


class InvalidPloomberResourcesException(BasePloomberCloudException):
    """Exception for invalid resource choices"""

    pass


class InternalServerErrorException(BasePloomberCloudException):
    """Exception for 500 errors"""

    def __init__(self):
        message = "Internal server error. Please contact support: contact@ploomber.io"
        super().__init__(message)


class UserTierForbiddenException(BasePloomberCloudException):
    """Exception for forbidden operations"""

    def __init__(self, permissions: t.List[str]):
        from ploomber_cloud.util import (
            camel_case_to_human_readable,
            get_user_type,
            get_user_types_with_allowed_permission,
        )

        user_type = get_user_type()
        valid_user_tiers = get_user_types_with_allowed_permission(permissions)
        message = (
            f"Your user tier ({user_type.value}) is not allowed to use these \
            feature(s):\n"
            + "\n".join(
                list(
                    map(
                        lambda perm: reduce(
                            lambda cur_str, func: func(cur_str),
                            [
                                camel_case_to_human_readable,
                                lambda to_bullet_point: f"- {to_bullet_point}",
                            ],
                            perm,
                        ),
                        permissions,
                    )
                )
            )
            + "\n"
            + "To use this feature, you must be one of the following user tiers: "
            + ",".join(list(map(lambda user: user.value, valid_user_tiers)))
            + "\n"
            + "Please contact support: contact@ploomber.io"
        )
        super().__init__(message)
