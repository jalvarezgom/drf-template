from actstream import action
from actstream.models import ActionEvent

from apps.core.audit.audit_events import AuditActions
from apps.authentication.models import User


class AuditActionsRepository:
    class User:
        @staticmethod
        def signup(user: User):
            action_event = ActionEvent.objects.get(pk=AuditActions.Events.User.SIGNUP)
            action.send(user, verb=action_event)

        @staticmethod
        def login_successful(user: User, ip: str):
            action_event = ActionEvent.objects.get(pk=AuditActions.Events.User.LOGIN)
            action.send(user, verb=action_event, ip=ip)

        @staticmethod
        def login_failed(request_data: dict, ip: str):
            try:
                user = User.objects.get(username=request_data.get("email"))
            except User.DoesNotExist:
                user = None

            if user:
                action_event = ActionEvent.objects.get(pk=AuditActions.Events.User.FAILED_LOGIN)
                action.send(user, verb=action_event, ip=ip)
