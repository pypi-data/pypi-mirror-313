# Generated by Django 3.2.13 on 2024-10-25 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ddm_logging', '0002_alter_exceptionlogentry_blueprint'),
        ('ddm_questionnaire', '0003_alter_questionbase_blueprint'),
        ('ddm', '0052_auto_20241025_1451'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(
                    name='DonationBlueprint',
                ),
                migrations.DeleteModel(
                    name='DonationInstruction',
                ),
                migrations.DeleteModel(
                    name='FileUploader',
                ),
                migrations.DeleteModel(
                    name='ProcessingRule',
                ),
            ],
            database_operations=[
                migrations.AlterModelTable(
                    name='DonationBlueprint',
                    table='ddm_datadonation_donationblueprint'
                ),
                migrations.AlterModelTable(
                    name='DonationInstruction',
                    table='ddm_datadonation_donationinstruction'
                ),
                migrations.AlterModelTable(
                    name='FileUploader',
                    table='ddm_datadonation_fileuploader'
                ),
                migrations.AlterModelTable(
                    name='ProcessingRule',
                    table='ddm_datadonation_processingrule'
                ),
            ]
        )
    ]
