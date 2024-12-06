from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lipetsk_specifics', '0008_add_privilege'),
        # Поставил эту зависимость, чтобы сначала данные скопировались в новую
        # таблицу, потом отработало удаление таблицы
        ('privilege_attributes', '0002_copy_data_from_lipetsk_table'),
    ]

    operations = [
        migrations.DeleteModel(name='PrivilegeConfirmationAttributes',),
    ]
