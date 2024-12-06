from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('smev3_v321', '0007_updateorderrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='declarationoriginmessageid',
            name='reviewed_sent',
            field=models.BooleanField(
                default=False,
                verbose_name='Показатель отправки сообщения changeOrderInfo'),
        ),
    ]
