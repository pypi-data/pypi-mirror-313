from django.db import migrations, models
import lipetsk_specifics.utils


class Migration(migrations.Migration):

    dependencies = [
        ('declaration', '0002_auto_20170206_1055'),
        ('users', '0002_notifications'),
        ('lipetsk_specifics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeclarationPassingSmev',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('declaration', models.ForeignKey(verbose_name='\u0417\u0430\u044f\u0432\u043b\u0435\u043d\u0438\u0435', to='declaration.Declaration', on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PassingSmev',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('request', models.FileField(upload_to=lipetsk_specifics.utils.get_upload_dir, max_length=150, verbose_name='\u0417\u0430\u043f\u0440\u043e\u0441')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0438 \u0432\u0440\u0435\u043c\u044f', db_index=True)),
                ('result', models.FileField(max_length=150, upload_to=lipetsk_specifics.utils.get_upload_dir, null=True, verbose_name='\u0417\u0430\u043f\u0440\u043e\u0441', blank=True)),
                ('department', models.ForeignKey(verbose_name='\u0412\u0435\u0434\u043e\u043c\u0441\u0442\u0432\u043e', to='lipetsk_specifics.Department', on_delete=models.CASCADE)),
                ('profile', models.ForeignKey(verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', to='users.UserProfile', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': '\u041e\u0431\u0440\u0430\u0449\u0435\u043d\u0438\u044f \u0432 \u043d\u0435 \u044d\u043b\u0435\u043a\u0442\u0440\u043e\u043d\u043d\u044b\u0435 \u0432\u0435\u0434\u043e\u043c\u0441\u0442\u0432\u0430',
            },
        ),
        migrations.AddField(
            model_name='declarationpassingsmev',
            name='passing_smev',
            field=models.ForeignKey(verbose_name='\u041e\u0431\u0440\u0430\u0449\u0435\u043d\u0438\u0435 \u0432 \u043d\u0435 \u044d\u043b\u0435\u043a\u0442\u0440\u043e\u043d\u043d\u044b\u0435 \u0432\u0435\u0434\u043e\u043c\u0441\u0442\u0432\u0430', to='lipetsk_specifics.PassingSmev', on_delete=models.CASCADE),
        ),
    ]
