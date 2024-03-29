# Generated by Django 3.2 on 2024-02-19 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_miniprogramaccount_account'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='class_code',
        ),
        migrations.RemoveField(
            model_name='account',
            name='faculty_code',
        ),
        migrations.RemoveField(
            model_name='account',
            name='major_code',
        ),
        migrations.RemoveField(
            model_name='account',
            name='student_num',
        ),
        migrations.AddField(
            model_name='account',
            name='school_num',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='学号/工号'),
        ),
        migrations.AlterField(
            model_name='account',
            name='type',
            field=models.CharField(default='', max_length=50, verbose_name='用户角色(学生或教职工或校外人员)'),
        ),
        migrations.DeleteModel(
            name='MiniprogramAccount',
        ),
    ]
