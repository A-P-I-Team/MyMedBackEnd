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
                # instance.nottakenno = 24 * instance.days // instance.period
                instance.nottakenno = 0

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
            if previous.status:
                # True --> None
                if instance.status is None:
                    PrescriptionMedicines.objects.filter(id=instance.prescription_medicine.id).update(
                        takenno=F('takenno') - 1,
                        nottakenno=F('nottakenno')
                    )

                # True --> False
                elif not instance.status:
                    PrescriptionMedicines.objects.filter(id=instance.prescription_medicine.id).update(
                        takenno=F('takenno') - 1,
                        nottakenno=F('nottakenno') + 1
                    )

            if instance.status:
                # None --> True
                if previous.status is None:
                    PrescriptionMedicines.objects.filter(id=instance.prescription_medicine.id).update(
                        takenno=F('takenno') + 1,
                        nottakenno=F('nottakenno')
                    )

                # False --> True
                elif not previous.status:
                    PrescriptionMedicines.objects.filter(id=instance.prescription_medicine.id).update(
                        takenno=F('takenno') + 1,
                        nottakenno=F('nottakenno') - 1
                    )

            # None --> False
            if instance.status == False and previous.status is None:
                PrescriptionMedicines.objects.filter(id=instance.prescription_medicine.id).update(
                    takenno=F('takenno'),
                    nottakenno=F('nottakenno') + 1
                )

            # False --> None
            if previous.status == False and instance.status is None:
                PrescriptionMedicines.objects.filter(id=instance.prescription_medicine.id).update(
                    takenno=F('takenno'),
                    nottakenno=F('nottakenno') - 1
                )
