# Copyright (c) 2024 Huawei Technologies Co., Ltd.
#
# openMind is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#
#          http://license.coscl.org.cn/MulanPSL2
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.
class OpenMindException(Exception):
    """
    Base class of exceptions, customize exceptions should inherit this class.
    If formatted exceptions needed, msg_fmt should be rewrited in subclasses.

    Examples:

    ```python
    >>> # define an exception
    >>> class FrameworkNotSupportedError(OpenMindException):
             msg_fmt = "Framework %(framework)s not supported."

    >>> # use the defined exception
    >>> raise FrameworkNotSupportedError(framework="AN_INVALID_FRAMEWORK")
    >>> # or use the exception directly without format string
    >>> raise FrameworkNotSupportedError("SOME ERROR MESSAGE")
    ```
    """

    msg_fmt = "An unknown exception occurred."

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        try:
            if not message:
                message = self.msg_fmt % kwargs
            else:
                message = str(message)
        except Exception:
            message = self.msg_fmt

        self.message = message
        super().__init__(message)

    def __repr__(self):
        dict_repr = self.__dict__
        dict_repr["class"] = self.__class__.__name__
        return str(dict_repr)


class InputValidationError(OpenMindException):
    msg_fmt = "Invalid input."


class FrameworkNotSupportedError(OpenMindException):
    msg_fmt = "Framework %(framework)s not supported, it should be in ['pt', 'ms']."


class NotFoundAnyFrameworkError(OpenMindException):
    msg_fmt = "Not found any framework in your environment."


class PackageNotFoundError(OpenMindException):
    msg_fmt = "Package %(package)s not found."


class PipelinePackageNotFoundError(PackageNotFoundError):
    msg_fmt = "%(pipeline)s pipeline wanted, but necessary package %(package)s not found."
