# Generated by Django 3.2.13 on 2024-10-25 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ddm_participation', '0001_initial'),
        ('ddm_datadonation', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='datadonation',
                    name='participant',
                    field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                            to='ddm_participation.participant'),
                ),
            ],
            # Reusing an existing table, so do nothing.
            database_operations=[]
        )
    ]
