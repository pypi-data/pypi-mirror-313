import logging
from functools import cached_property


class LoggerMixin:  # pylint: disable=too-few-public-methods
    """Simple mixin for logging.

    Adds a ``logger`` property to the class and sets the logger name
    to the module and class name of the class:

        >>> class MyClass(LoggerMixin):
        ...     pass
        ...
        >>> my_class = MyClass()
        >>> my_class.logger.name
        'mymodule.MyClass'
    """

    @cached_property
    def logger(self) -> logging.Logger:
        """
        Logger instance for this class.

        The logger name is determined by the module and class name of this class.
        For example, if the class is named `MyClass` and it's in the module
        `mymodule`, the logger name will be `mymodule.MyClass`.

        Returns:
            Logger: Logger instance for this class.
        """
        name = ".".join([self.__class__.__module__, self.__class__.__name__])
        return logging.getLogger(name)
