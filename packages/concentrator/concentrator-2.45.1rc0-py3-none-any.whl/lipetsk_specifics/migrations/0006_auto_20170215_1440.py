from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lipetsk_specifics', '0005_auto_20170208_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='privilegeconfirmationattributes',
            name='document',
            field=models.CharField(
                max_length=100, null=True,
                verbose_name='Удостоверение', blank=True),
        ),
        migrations.AddField(
            model_name='privilegeconfirmationattributes',
            name='military_document',
            field=models.CharField(
                max_length=100, null=True,
                verbose_name='Военный билет', blank=True),
        ),
        migrations.AddField(
            model_name='privilegeconfirmationattributes',
            name='name_of_unit',
            field=models.CharField(
                max_length=150,  null=True,
                verbose_name='Наименование подразделения', blank=True),
        ),
        migrations.AddField(
            model_name='privilegeconfirmationattributes',
            name='ovd',
            field=models.CharField(
                max_length=150, null=True,
                verbose_name='ОВД, выдавшее удостоверение', blank=True),
        ),
    ]
