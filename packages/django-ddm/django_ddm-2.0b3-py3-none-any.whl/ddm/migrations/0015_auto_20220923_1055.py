# Generated by Django 3.2.13 on 2022-09-23 08:55

import ddm.participation.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddm', '0014_auto_20220922_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='donationproject',
            name='expected_url_parameters',
            field=models.CharField(blank=True, help_text='Separate multiple parameters with a semikolon (";"). Semikolons are not allowed as part of the expected url parameters.', max_length=500, null=True, verbose_name='Expected URL parameter'),
        ),
        migrations.AddField(
            model_name='donationproject',
            name='url_parameter_enabled',
            field=models.BooleanField(default=False, verbose_name='URL parameter extraction enabled'),
        ),
        migrations.AddField(
            model_name='participant',
            name='extra_data',
            field=models.JSONField(default=ddm.participation.models.get_extra_data_default),
        ),
    ]
