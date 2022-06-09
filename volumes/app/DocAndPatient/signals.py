from datetime import datetime, timedelta, timezone

from django.db.models import F
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from DocAndPatient.models import PrescriptionMedicines, Reminder


@receiver(pre_save, sender=PrescriptionMedicines)
def reminders(sender, **kwargs):
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
                        prescription_medicine=instance,
                        date_time=instance.start + timedelta(hours=i * instance.period),
                        status=None
                    )
                # Set NotTakenNo
                instance.nottakenno = 24 * instance.days // instance.period

            if previous.start is not None:
                if instance.start is None:
                    # Delete Reminders
                    Reminder.objects.filter(prescription_medicine=instance.id).delete()
                    # Reset TakenNo & NotTakenNo
                    instance.nottakenno = 0
                    instance.takenno = 0

                if instance.start is not None:
                    # Update Reminders
                    Reminder.objects.filter(prescription_medicine=instance.id).update(
                        date_time=F('date_time') + (instance.start - previous.start),
                        status=None
                    )
                    # Reset TakenNo & NotTakenNo
                    instance.nottakenno = 0
                    instance.takenno = 0


@receiver(pre_save, sender=Reminder)
def statistic(sender, **kwargs):
    instance: Reminder = kwargs.get('instance')

    if instance.id is None:
        pass
    else:
        # Update Instance
        previous = Reminder.objects.get(id=instance.id)
        if previous.status != instance.status:
            # True --> False OR True --> None
            if previous.status and (not instance.status or instance.status is None):
                PrescriptionMedicines.objects.filter(id=instance.prescription_medicine.id).update(
                    takenno=F('takenno') - 1,
                    nottakenno=F('nottakenno') + 1
                )

            # False --> True OR None --> True
            if instance.status and (not previous.status or previous.status is None):
                PrescriptionMedicines.objects.filter(id=instance.prescription_medicine.id).update(
                    takenno=F('takenno') + 1,
                    nottakenno=F('nottakenno') - 1
                )
