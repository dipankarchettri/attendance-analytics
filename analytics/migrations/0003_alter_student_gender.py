# Generated by Django 5.0.4 on 2024-05-07 18:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("analytics", "0002_alter_student_date_of_birth_alter_student_email_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="gender",
            field=models.CharField(
                choices=[("M", "Male"), ("F", "Female"), ("O", "Other")], max_length=1
            ),
        ),
    ]
