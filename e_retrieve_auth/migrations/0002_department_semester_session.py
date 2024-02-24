# Generated by Django 4.2.4 on 2023-08-23 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("e_retrieve_auth", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Department",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Department_title", models.CharField(max_length=100, unique=True)),
            ],
            options={"verbose_name_plural": "Departments", "db_table": "Department",},
        ),
        migrations.CreateModel(
            name="Semester",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("semester_title", models.CharField(max_length=20, unique=True)),
            ],
            options={"verbose_name_plural": "Semesters", "db_table": "Semester",},
        ),
        migrations.CreateModel(
            name="Session",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("session_title", models.CharField(max_length=9, unique=True)),
                (
                    "session_description",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
            ],
            options={"verbose_name_plural": "Sessions", "db_table": "Session",},
        ),
    ]
