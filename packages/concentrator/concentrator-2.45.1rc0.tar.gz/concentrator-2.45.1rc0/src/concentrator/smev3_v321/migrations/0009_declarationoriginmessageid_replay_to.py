from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('smev3_v321', '0008_declarationoriginmessageid_reviewed_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='declarationoriginmessageid',
            name='replay_to',
            field=models.CharField(max_length=4000,
                                   null=True,
                                   verbose_name='Индекс сообщения в СМЭВ'),
        ),
    ]
