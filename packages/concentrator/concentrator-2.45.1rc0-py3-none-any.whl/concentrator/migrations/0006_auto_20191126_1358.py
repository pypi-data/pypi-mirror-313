from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concentrator', '0005_migrate_model_fields_in_changedeclaration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='changedeclaration',
            name='commentary',
            field=models.TextField(blank=True,
                                   null=True,
                                   verbose_name='Комментарий'),
        ),
    ]
