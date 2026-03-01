class DRFActionType:
    DEFAULT = "default"
    LIST = "list"
    RETRIEVE = "retrieve"
    CREATE = "create"
    UPDATE = "update"
    PARTIAL_UPDATE = "partial_update"
    DESTROY = "destroy"
    DATATABLE = "datatable"
    SELECT = "select"

    @classmethod
    def get_conditions(cls, action):
        from apps.core.libs.ViewSetScenarios.conditions import DRFScenariosCondition

        return {
            DRFActionType.DATATABLE: DRFScenariosCondition.datatable,
            DRFActionType.SELECT: DRFScenariosCondition.select,
            DRFActionType.LIST: DRFScenariosCondition.list,
        }.get(action, DRFScenariosCondition.action)
