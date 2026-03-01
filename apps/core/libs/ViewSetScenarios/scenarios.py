from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import Serializer

from apps.core.libs.ViewSetScenarios.action_type import DRFActionType
from apps.core.libs.ViewSetScenarios.exceptions import ViewSetScenarioNotFound, ViewSetScenarioException


class DRFScenario:
    def __init__(self, action, serializer, pagination=None, condition=None):
        if action is None:
            raise ViewSetScenarioException("Action must be defined")
        self.action = action
        if condition is None:
            condition = DRFActionType.get_conditions(action)
        if not callable(condition):
            raise ViewSetScenarioException("Condition must be a callable")
        self.condition = condition
        if not issubclass(serializer, Serializer):
            raise ViewSetScenarioException("Serializer must be a Serializer class")
        self.serializer = serializer
        if pagination is not None and not issubclass(pagination, PageNumberPagination):
            raise ViewSetScenarioException("Pagination must be a PageNumberPagination class or None")
        self.pagination = pagination

    def __repr__(self):
        return f"{self.__class__.__name__}({self.action})"


class DRFDirectorScenarios:
    paginations = None
    serializers = None
    actions = None

    def __init__(self, drf_scenarios: list[DRFScenario] = None):
        if drf_scenarios is None:
            drf_scenarios = []
        if drf_scenarios:
            self.set_scenarios(drf_scenarios)

    def set_scenarios(self, scenarios):
        serializer_scenarios_class, pagination_scenarios_class, action_scenarios_class = {}, {}, {}
        for sce in scenarios:
            serializer_scenarios_class[sce.action] = sce.serializer
            if sce.pagination:
                pagination_scenarios_class[sce.action] = sce.pagination
            action_scenarios_class[sce.action] = sce.condition
        self.set_serializers(serializer_scenarios_class)
        self.set_paginations(pagination_scenarios_class)
        self.set_actions(action_scenarios_class)

    def get_action(self, action, request, *args, **kwargs):
        result = DRFActionType.DEFAULT
        for scenario, sce_condition in self.actions.items():
            if sce_condition(action, request, scenario, *args, **kwargs):
                result = scenario
                break
        return result

    def set_actions(self, actions):
        self.actions = actions

    def get_pagination(self, scenario):
        pagination_class = self.paginations.get(scenario, None)
        return pagination_class

    def set_paginations(self, paginations):
        self.paginations = paginations if len(paginations.keys()) > 0 else None

    def get_serializer(self, scenario, action):
        serializer_class = self.serializers.get(scenario, None)
        if serializer_class is None:
            raise ViewSetScenarioNotFound(f"Action {action} - Serializer scenario '{scenario}' not found")
        return serializer_class

    def set_serializers(self, serializers):
        self.serializers = serializers

    def __repr__(self):
        return f"{self.__class__.__name__}(actions=[{', '.join(self.actions.keys())}])"
