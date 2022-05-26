from datetime import datetime, timedelta, timezone

from django.db.models import F
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from DocAndPatient.models import PrescriptionMedicines, Reminder


# TODO
@receiver(pre_save, sender=PrescriptionMedicines)
def function(sender, **kwargs):
    instance: PrescriptionMedicines = kwargs.get('instance')

    # Create Instance
    if instance.id is None:
        pass
    else:
        # Update Instance
        previous = PrescriptionMedicines.objects.get(id=instance.id)
        if previous.start != instance.start:
            if previous.start is None:
                # Create Reminders
                for i in range(24 * instance.days // instance.period):
                    Reminder.objects.create(
                        prescription_medicine=instance.id,
                        date_time=instance.start + timedelta(hours=i * instance.period),
                        status=None
                    )

            if previous.start is not None:
                if instance.start is None:
                    # Delete Reminders
                    Reminder.objects.filter(prescription_medicine=instance.id).delete()

                if instance.start is not None:
                    # Update Reminders
                    Reminder.objects.filter(prescription_medicine=instance.id).update(
                        date_time=F('date_time') + (instance.start - previous.start),
                        status=None
                    )
