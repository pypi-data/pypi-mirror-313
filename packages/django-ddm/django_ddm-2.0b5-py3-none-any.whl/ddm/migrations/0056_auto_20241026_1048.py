# Generated by Django 3.2.13 on 2024-10-26 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ddm_participation', '0002_alter_participant_project'),
        ('ddm_questionnaire', '0005_auto_20241026_1048'),
        ('ddm_datadonation', '0003_auto_20241026_1048'),
        ('ddm_logging', '0004_auto_20241026_1048'),
        ('ddm_auth', '0002_alter_projectaccesstoken_project'),
        ('ddm', '0055_delete_participant'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(
                    model_name='researchprofile',
                    name='user',
                ),
                migrations.DeleteModel(
                    name='DonationProject',
                ),
                migrations.DeleteModel(
                    name='ResearchProfile',
                ),
            ],
            database_operations=[
                migrations.AlterModelTable(
                    name='DonationProject',
                    table='ddm_projects_donationproject'
                ),
                migrations.AlterModelTable(
                    name='ResearchProfile',
                    table='ddm_projects_researchprofile'
                ),
            ]
        )
    ]
