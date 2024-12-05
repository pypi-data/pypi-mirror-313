# Generated by Django 3.2.13 on 2024-10-26 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ddm_projects', '0001_initial'),
        ('ddm_datadonation', '0002_alter_datadonation_participant'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='datadonation',
                    name='project',
                    field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ddm_projects.donationproject'),
                ),
                migrations.AlterField(
                    model_name='donationblueprint',
                    name='project',
                    field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ddm_projects.donationproject'),
                ),
                migrations.AlterField(
                    model_name='fileuploader',
                    name='project',
                    field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ddm_projects.donationproject'),
                ),
            ],
            # Reusing an existing table, so do nothing.
            database_operations=[]
        )
    ]
