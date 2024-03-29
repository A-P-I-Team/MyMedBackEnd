# Generated by Django 4.0.4 on 2022-05-29 14:01

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('User', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('msn', models.CharField(blank=True, max_length=10, null=True, unique=True, validators=[django.core.validators.RegexValidator(regex='^[0-9]{10}$')])),
                ('degree', models.CharField(blank=True, choices=[('GP', 'General Practitioner'), ('SP', 'Specialist'), ('SS', 'Sub-Specialist')], max_length=2, null=True)),
                ('field', models.CharField(blank=True, choices=[('CAR', 'Cardiologist'), ('NEU', 'Neurologist'), ('GYN', 'Geynecologist'), ('OBS', 'Obstetrician'), ('PED', 'Pediatrician'), ('URO', 'Urologists'), ('OTL', 'Otolaryngologist'), ('INF', 'Infection Disease'), ('INT', 'Internal Medicine'), ('SUR', 'Surgeon'), ('RAL', 'Radiologist'), ('RAT', 'Radiotherapy'), ('PHY', 'Physiologist'), ('ORT', 'Orthopedist'), ('PAT', 'Pathology')], max_length=3, null=True)),
                ('experience', models.IntegerField(blank=True, null=True)),
                ('about', models.TextField(blank=True, null=True)),
                ('hours_of_work', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=11, null=True, unique=True, validators=[django.core.validators.RegexValidator(regex='^[0-9]{11}$')])),
                ('officeno', models.CharField(blank=True, max_length=11, null=True, unique=True, validators=[django.core.validators.RegexValidator(regex='^[0-9]{11}$')])),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('User.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('type', models.CharField(choices=[('A', 'Ampoule'), ('T', 'Tablet'), ('S', 'Syrup')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prescriptionsofdoctor', to='DocAndPatient.doctor')),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prescriptionsofpatient', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PrescriptionMedicines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dosage', models.PositiveSmallIntegerField()),
                ('fraction', models.CharField(choices=[('1/4', '1 Quarter'), ('1/2', '2 Quarter'), ('3/4', '3 Quarter'), ('1', '4 Quarter')], default='1', max_length=3)),
                ('days', models.PositiveSmallIntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='prescriptions', to='DocAndPatient.medicine')),
                ('prescription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medicines', to='DocAndPatient.prescription')),
            ],
        ),
    ]
