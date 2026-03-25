from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("checkout", "0002_classbooking_course_nullable"),
    ]

    operations = [
        migrations.AddField(
            model_name="classbooking",
            name="confirmation_email_sent",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="classbooking",
            name="confirmation_email_sent_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
