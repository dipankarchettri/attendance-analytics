# Generated by Django 5.0.4 on 2024-05-09 18:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("analytics", "0003_alter_student_gender"),
    ]

    operations = [
        migrations.AddField(
            model_name="attendance",
            name="day_of_week",
            field=models.CharField(max_length=10, null=True),
        ),
    ]
