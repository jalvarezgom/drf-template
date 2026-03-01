from apps.core.libs.ViewSetScenarios.exceptions import ViewSetScenarioException
from apps.core.libs.ViewSetScenarios.scenarios import DRFDirectorScenarios


class ViewSetScenarios:
    director_class = DRFDirectorScenarios
    _pagination_scenarios_class = None
    _serializer_scenarios_class = None
    _action_scenarios_class = None

    def __init__(self, scenarios=None, *args, **kwargs):
        self.director_class = self.director_class()
        if scenarios:
            self.director_class.set_scenarios(scenarios)

    def get_paginator(self, viewset):
        if viewset.pagination_class is not None:
            viewset._paginator = getattr(viewset, "_paginator", None) or viewset.pagination_class()
            return viewset._paginator
        _paginator = None
        if self.director_class.paginations is not None:
            scenario = self.director_class.get_action(viewset.action, viewset.request)
            _paginator = self.director_class.get_pagination(scenario)()
        return _paginator

    def get_serializer_class(self, viewset):
        if getattr(viewset, "serializer_class", None):  # viewset.serializer_class:
            return viewset.serializer_class
        scenario = self.director_class.get_action(viewset.action, viewset.request)
        serializer_class = self.director_class.get_serializer(scenario, viewset.action)
        if serializer_class is None:
            raise ViewSetScenarioException(
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method." % self.__class__.__name__
            )
        return serializer_class

    def __repr__(self):
        return f"{self.__class__.__name__}({self.director_class})"
