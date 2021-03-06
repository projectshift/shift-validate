from abc import ABCMeta, abstractmethod


class AbstractFilter(metaclass=ABCMeta):
    """
    Abstract filter
    Provides a base for concrete filters and your custom filters. All
    of those can be added to simple properties on the processor.
    """

    @abstractmethod
    def filter(self, value, model=None, context=None):
        """
        Filter
        Abstract filtering method: implement this in your concrete
        filters. Accepts a value and returns filtered value.

        :param value:               a value to filter
        :param model:               parent model of the property
        :param context:             parent model or custom context
        :return:                    filtered value
        """
        raise NotImplemented



