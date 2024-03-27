# Generated by Django 5.0.1 on 2024-03-26 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_image_bannerimage_full_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_desired', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('street_address', models.CharField(max_length=255)),
                ('address_line_2', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(max_length=100)),
                ('state_province_region', models.CharField(max_length=100)),
                ('zip_postal_code', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('referred_by', models.CharField(blank=True, max_length=100, null=True)),
                ('convicted', models.BooleanField()),
                ('school_name', models.CharField(max_length=100)),
                ('highest_grade_completed', models.CharField(max_length=20)),
                ('graduate', models.BooleanField()),
                ('consent', models.BooleanField()),
                ('resume', models.FileField(upload_to='resumes/')),
                ('class_schedule', models.FileField(upload_to='class_schedules/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
