from django.db.models import signals
from django.dispatch import receiver

from core.models import Country


@receiver(signals.post_save, sender=Country)
def country_created(sender, instance, **kwargs):
    print("created",str(sender), str(instance.name))


