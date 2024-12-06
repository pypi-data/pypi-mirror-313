from django.db import migrations
from django.db import models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('direct', '0013_change_direct_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicantAnswer',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('answer',
                 models.BooleanField(verbose_name='Ответ заявителя')),
                ('comment',
                 models.CharField(blank=True,
                                  max_length=2048,
                                  null=True,
                                  verbose_name='Комментарий заявителя')),
                ('direct',
                 models.OneToOneField(
                     on_delete=django.db.models.deletion.CASCADE,
                     related_name='smev3_v321_applicant_answer',
                     to='direct.Direct',
                     verbose_name='Направление')),
            ],
            options={
                'verbose_name': 'Ответ заявителя',
                'db_table': 'concentrator_smev3_v321_applicantanswer',
            },
        ),
    ]
