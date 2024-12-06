from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('children', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('declaration', '0001_initial'),
        ('concentrator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='docextrainfo',
            name='declaration',
            field=models.ForeignKey(to='declaration.Declaration', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='delegateperson',
            name='delegate',
            field=models.OneToOneField(related_name='concentrator_delegate', null=True, blank=True, to='children.Delegate', on_delete=models.SET_NULL),
        ),
        migrations.AddField(
            model_name='changedeclaration',
            name='declaration',
            field=models.ForeignKey(to='declaration.Declaration', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='changedeclaration',
            name='user',
            field=models.ForeignKey(verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL),
        ),
    ]
