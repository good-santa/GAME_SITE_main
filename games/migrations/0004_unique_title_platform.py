from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_game_original_price'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='game',
            unique_together={('title', 'platform')},
        ),
    ]

