from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_remove_game_created_at_remove_game_release_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='original_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]

