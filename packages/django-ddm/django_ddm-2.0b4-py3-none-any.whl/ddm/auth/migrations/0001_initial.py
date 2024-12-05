# Generated by Django 3.2.13 on 2024-10-25 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ddm', '0049_delete_projectaccesstoken'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='ProjectAccessToken',
                    fields=[
                        ('key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                        ('created', models.DateTimeField(auto_now_add=True)),
                        ('expiration_date', models.DateTimeField(blank=True, null=True)),
                        ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,
                                                         related_name='donation_project', to='ddm.donationproject',
                                                         verbose_name='Donation Project')),
                    ],
                )
            ],
            # Table already exists. See ddm/migrations/0049_delete_projectaccesstoken.py (may be moved to ddm.core)
            database_operations = [],
        )
    ]
