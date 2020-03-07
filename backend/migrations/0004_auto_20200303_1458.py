# Generated by Django 2.2.10 on 2020-03-03 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20200228_1818'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='email',
            field=models.CharField(default='', max_length=50, verbose_name='邮箱'),
        ),
        migrations.AddField(
            model_name='student',
            name='phone',
            field=models.CharField(default='', max_length=11, verbose_name='手机号'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='email',
            field=models.CharField(default='', max_length=50, verbose_name='邮箱'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='phone',
            field=models.CharField(default='', max_length=11, verbose_name='手机号'),
        ),
        migrations.AlterField(
            model_name='selection',
            name='pass_status',
            field=models.IntegerField(choices=[(0, '通过'), (1, '待通过'), (2, '未通过')], default=0, verbose_name='通过情况'),
        ),
    ]
