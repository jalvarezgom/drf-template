import datetime

from actstream.managers import ActionManager, stream


class AuditManager(ActionManager):
    @stream
    def stream_data(self, obj, verb, time=None):
        if time is None:
            time = datetime.datetime.now()
        return obj.actor_actions.filter(verb=verb, timestamp_lte=time)
