from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0001_initial"),
        ("checkout", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="classbooking",
            name="course",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="bookings",
                to="services.exerciseclass",
            ),
        ),
    ]
