from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lipetsk_specifics',
         '0009_delete_privilegeconfirmationattributes_model'),
        # Cначала копируем данные в другую таблицу, потом удаляем
        ('declaration', '0031_copy_data_from_lipetsk_tables'),
    ]

    operations = [
        migrations.DeleteModel(name='DeclarationRejectReason', ),
        migrations.DeleteModel(name='RejectReason', ),
    ]
