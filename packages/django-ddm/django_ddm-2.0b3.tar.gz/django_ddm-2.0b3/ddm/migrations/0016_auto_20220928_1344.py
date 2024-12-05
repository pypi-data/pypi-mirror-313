# Generated by Django 3.2.13 on 2022-09-28 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ddm', '0015_auto_20220923_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donationproject',
            name='redirect_target',
            field=models.CharField(blank=True, help_text='Always include <i>http://</i> or <i>https://</i> in the redirect target. If URL parameter extraction is enabled for this project, you can include the extracted URL parameters in the redirect target as follows: "https://redirect.me/?redirectpara=<b>{{URLParameter}}</b>".', max_length=2000, null=True, verbose_name='Redirect target'),
        ),
        migrations.CreateModel(
            name='ProcessingRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('field', models.TextField()),
                ('execution_order', models.IntegerField()),
                ('input_type', models.CharField(choices=[('number', 'Number'), ('date', 'Date'), ('string', 'String')], default='string', max_length=10)),
                ('comparison_operator', models.CharField(choices=[('==', 'Equal (==)'), ('!=', 'Not Equal (!=)'), ('>', 'Greater than (>)'), ('<', 'Smaller than (<)'), ('>=', 'Greater than or equal (>=)'), ('<=', 'Smaller than or equal (<=)'), ('regex', 'Regex (removes matches)')], default='==', max_length=10)),
                ('comparison_value', models.TextField()),
                ('blueprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ddm.donationblueprint')),
            ],
        ),
    ]
