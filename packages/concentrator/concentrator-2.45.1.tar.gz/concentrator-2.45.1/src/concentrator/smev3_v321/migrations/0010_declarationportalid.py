from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('smev3_v321', '0009_declarationoriginmessageid_replay_to'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeclarationPortalID',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('portal_id',
                 models.CharField(
                     max_length=100,
                     unique=True,
                     verbose_name='Идентифкатор заявления на портале')),
                ('declaration',
                 models.OneToOneField(
                     on_delete=models.deletion.CASCADE,
                     to='declaration.Declaration')),
            ],
        ),
    ]
