import factory
from django_celery_beat.models import IntervalSchedule, PeriodicTask, CrontabSchedule


class CrontabScheduleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CrontabSchedule
        django_get_or_create = (
            "minute",
            "hour",
            "day_of_week",
            "day_of_month",
            "month_of_year",
        )


class IntervalScheduleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IntervalSchedule
        django_get_or_create = (
            "every",
            "period",
        )


class PeriodicTaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PeriodicTask
        django_get_or_create = ("name",)


def get_scheduled_tasks():
    scheduled_tasks = [
        # PeriodicTaskFactory(
        #     task="api.example",
        #     name="update_trending_counters",
        #     interval=IntervalScheduleFactory(every=1, period=IntervalSchedule.DAYS),
        #     expire_seconds=60 * 60 * 2,  # 2 hours
        # ),
    ]

    return scheduled_tasks
