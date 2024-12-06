from django.db import migrations, models
import django.db.models.deletion
import kinder.core.db


class Migration(migrations.Migration):

    dependencies = [
        ('concentrator', '0002_auto_20170206_1055'),
        ('lipetsk_specifics', '0006_auto_20170215_1440'),
    ]

    operations = [
        migrations.CreateModel(
            name='Changes',
            fields=[
                ('id', models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')),
                ('change_declaration', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='change_declaration',
                    to='concentrator.ChangeDeclaration')),
            ], ),
    ]
