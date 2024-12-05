# Generated by Django 3.2.13 on 2024-10-25 09:19

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ddm', '0050_auto_20241025_1119'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='ExceptionLogEntry',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('date', models.DateTimeField(default=django.utils.timezone.now)),
                        ('raised_by', models.CharField(blank=True, choices=[('server', 'Server'), ('client', 'Client')], max_length=20)),
                        ('exception_type', models.IntegerField(null=True)),
                        ('message', models.TextField()),
                        ('blueprint', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ddm.donationblueprint')),
                        ('participant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ddm.participant')),
                        ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ddm.donationproject')),
                    ],
                ),
                migrations.CreateModel(
                    name='EventLogEntry',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('date', models.DateTimeField(default=django.utils.timezone.now)),
                        ('description', models.TextField()),
                        ('message', models.TextField()),
                        ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ddm.donationproject')),
                    ],
                ),
            ],
            # Table already exists. See ddm/migrations/0050_auto_20241025_1119.py (may be moved to ddm.core)
            database_operations=[],
        )
    ]
