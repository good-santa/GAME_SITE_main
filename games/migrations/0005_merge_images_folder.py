from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_unique_title_platform'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='game',
            name='screenshot',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]

