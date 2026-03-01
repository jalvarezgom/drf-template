from actstream.models import ActionEvent

from apps.core.audit.audit_events import AuditActions
from seroil_gas_ahorro.management.commands.seeders.base import SeederData


class SeederStaticData(SeederData):
    @classmethod
    def _prepare_data(cls):
        cls._audit_events = {
            AuditActions.Categories.User: AuditActions.Events.User,
        }

    @classmethod
    def run(cls):
        cls._prepare_data()
        cls._load_audit_events()

    @classmethod
    def _load_audit_events(cls):
        for category, actions in cls._audit_events.items():
            for event in actions:
                ActionEvent.objects.get_or_create(
                    pk=event.value,
                    defaults={
                        "entity_name": category,
                        "message": event.msg,
                    },
                )
