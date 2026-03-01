class DRFScenariosCondition:
    @classmethod
    def datatable(cls, action, request, *args, **kwargs):
        return action == "list" and request.query_params.get("scenario", None) == "datatable"

    @classmethod
    def select(cls, action, request, *args, **kwargs):
        return action == "list" and request.query_params.get("scenario", None) == "select"

    @classmethod
    def list(cls, action, request, *args, **kwargs):
        return action == "list" and request.query_params.get("scenario", None) not in ("datatable", "select")

    @classmethod
    def action(cls, action, request, scenario, *args, **kwargs):
        return action == scenario
